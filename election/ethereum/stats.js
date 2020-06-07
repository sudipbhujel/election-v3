import election from './election';
// import web3 from 'web3';

let totalCandidate;
let totalVoter;
let voteDropped;

async function stats() {
    totalCandidate = await election.methods.totalCandidate().call();
    totalVoter = await election.methods.totalVoter().call();
    voteDropped = await election.methods.voteDropped().call();
}

stats();

export { totalCandidate, totalVoter, voteDropped };