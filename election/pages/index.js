import React from 'react';
import election from '../ethereum/election';
import Layout from '../components/Layout';
import { Card } from 'semantic-ui-react';
import web3 from '../ethereum/web3';

import { Link } from '../routes';

class ElectionIndex extends React.Component {
    static async getInitialProps() {
        let candidates = [];
        const manager = await election.methods.manager().call();
        const accounts = await web3.eth.getAccounts();
        const totalCandidate = await election.methods.totalCandidate().call();
        const totalVoter = await election.methods.totalVoter().call();
        for (let i = 0; i < parseInt(totalCandidate); i++) {
            const candidate = await election.methods.candidates(i).call();
            const candidateAddress = candidate.candidateAddress;
            candidates.push(candidateAddress);
        }

        return { accounts, manager, totalCandidate, totalVoter, candidates };
    }

    renderCandidates() {
        const items = this.props.candidates.map(address => {
            return {
                header: address,
                meta: 'Candidate',
                fluid: true
            }
        });
        return <Card.Group items={items} />
    }

    render() {
        console.log(this.props.accounts);
        return (
            <Layout>
                <h2>Manager: {this.props.manager}</h2>
                <h2>Account: {this.props.accounts[0]}</h2>

                <h3>Total Candidates: {this.props.totalCandidate}</h3>
                <h3>Total Voter: {this.props.totalVoter}</h3>
                {this.renderCandidates()}

                <Link route={`/candidates/new`}>
                    <a>New Candidate</a>
                </Link>
                <Link route={`/voters/new`}>
                    <a>New Voter</a>
                </Link>

            </Layout>
        );
    };
}

export default ElectionIndex;