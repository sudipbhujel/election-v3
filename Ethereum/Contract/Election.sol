// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.4.22 <0.7.0;


contract Election {
    address public manager;
    uint256 public totalVoter;
    uint256 public totalCandidate;
    uint256 public voteDropped;

    enum State {Created, Voting, Ended}
    State public state;

    struct Voter {
        address voterAddress;
        bool isVoter;
        bool voted;
    }

    struct Candidate {
        address candidateAddress;
        uint256 totalVoteCount;
        bool isCandidate;
    }

    mapping(address => Voter) public voters;
    mapping(uint256 => Candidate) public candidates;

    constructor() public {
        manager = msg.sender;
        state = State.Created;
        totalVoter = 0;
        totalCandidate = 0;
        voteDropped = 0;
    }

    modifier onlyManager() {
        require(msg.sender == manager, "Manager only has persmission.");
        _;
    }

    modifier inState(State _state) {
        require(state == _state, "Election phase restriction.");
        _;
    }

    modifier notVoted() {
        require(
            voters[msg.sender].voted == false,
            "The voter who has not voted can cast vote."
        );
        _;
    }

    modifier isVoter() {
        require(voters[msg.sender].isVoter, "User must be voter");
        _;
    }

    event voterAdded(address _voter);
    event candidateAdded(address _candidate);
    event voteStarted();
    event voteDone(address voter);
    event voteEnded();

    function addVoter(address _voterAddress)
        public
        inState(State.Created)
        onlyManager
    {
        voters[_voterAddress] = Voter({
            voterAddress: _voterAddress,
            isVoter: true,
            voted: false
        });

        totalVoter++;

        emit voterAdded(_voterAddress);
    }

    function addCandidate(address _candidateAddress)
        public
        inState(State.Created)
        onlyManager
    {
        candidates[totalCandidate] = Candidate({
            candidateAddress: _candidateAddress,
            totalVoteCount: 0,
            isCandidate: true
        });

        voters[_candidateAddress] = Voter({
            voterAddress: _candidateAddress,
            isVoter: true,
            voted: false
        });

        totalCandidate++;
        totalVoter++;

        emit candidateAdded(_candidateAddress);
    }

    function startVote() public inState(State.Created) onlyManager {
        state = State.Voting;
        emit voteStarted();
    }

    function doVote(uint256 index)
        public
        inState(State.Voting)
        notVoted
        isVoter
    {
        require(candidates[index].isCandidate, "User must be candidate");

        voters[msg.sender].voted = true;
        candidates[index].totalVoteCount++;

        voteDropped++;

        emit voteDone(msg.sender);
    }

    function endVote()
        public
        inState(State.Voting)
        onlyManager
        returns (uint256)
    {
        state = State.Ended;
        return voteDropped;
    }
}
