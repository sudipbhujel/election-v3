const assert = require('assert');
const ganache = require('ganache-cli');
const Web3 = require('web3');
const web3 = new Web3(ganache.provider());

const compiledElection = require("../ethereum/build/Election.json");

let accounts;

beforeEach(async () => {
    accounts = await web3.eth.getAccounts();

    election = await new web3.eth.Contract(compiledElection.interface)
        .deploy({
            data: compiledElection.bytecode
        })
        .send({
            from: accounts[0],
            gas: '3000000'
        });

    // console.log(election)
});

describe('Election', () => {
    it('deploys a election', () => {
        assert.ok(election.options.address);
    });
    it('adds candidate', async () => {
        await election.methods.addCandidate(accounts[1]).send(
            { from: accounts[0], gas: '1000000' }
        );
        const totalCandidate = await election.methods.totalCandidate().call();
        const totalVoter = await election.methods.totalVoter().call();
        const candidate = await election.methods.candidates(0).call();
        assert.equal(candidate.candidateAddress, accounts[1]);
        assert.equal(totalCandidate, 1);
        assert.equal(totalVoter, 1)

    });
    it('adds voter', async () => {
        await election.methods.addVoter(accounts[1]).send(
            { from: accounts[0], gas: '1000000' }
        );
        const totalVoter = await election.methods.totalVoter().call();
        assert.equal(totalVoter, 1)
    })

    // it('allows people to contribute money and marks them as approvers', async () => {
    //     await campaign.methods.contribute().send({
    //         from: accounts[1],
    //         value: '200'
    //     });
    //     const isContributor = await campaign.methods.approvers(accounts[1]).call();
    //     assert(isContributor);
    // });

    // it('requires a minimum contribtion', async () => {
    //     try {
    //         await campaign.methods.contrubute().send({
    //             from: accounts[1],
    //             value: '5'
    //         });
    //         assert(false);
    //     } catch (error) {
    //         assert(error);
    //     }
    // });

    // it('allows a manager to make a payment request', async () => {
    //     await campaign.methods.createRequest('Buy batteries', '100', accounts[1]).send({
    //         from: accounts[0],
    //         gas: '3000000'
    //     });
    //     const request = await campaign.methods.requests(0).call();
    //     assert.equal('Buy batteries', request.description);
    // });

    // it('processes requests', async () => {
    //     await campaign.methods.contrubute().send({
    //         form: accounts[0],
    //         value: web3.utils.toWei('10', 'ether')
    //     });

    //     await campaign.methods.createRequest('A', web3.utils.toWei('5', 'ether'), accounts[1])
    //         .send(
    //             { from: accounts[0], gas: '3000000' }
    //         );

    //     await campaign.methods.approveRequest(0).send(
    //         { from: accounts[0], gas: '3000000' }
    //     );

    //     await campaign.methods.finalizeRequest(0).send(
    //         { from: accounts[0], gas: '3000000' }
    //     );

    //     let balance = await web3.eth.getBalance(accounts[1]);
    //     balance = web3.utils.fromWei(balance, 'ether');
    //     balance = parseFloat(balance);

    //     console.log(balance);
    //     assert(balance > 104);
    // });
});