import React from 'react';
import election from '../ethereum/election';
import Layout from '../components/Layout';
import { Card } from 'semantic-ui-react';

class ElectionIndex extends React.Component {
    static async getInitialProps() {
        let candidates = [];
        const totalCandidate = await election.methods.totalCandidate().call();
        const totalVoter = await election.methods.totalVoter().call();
        for (let i = 0; i < parseInt(totalCandidate); i++) {
            const candidate = await election.methods.candidates(i).call();
            const candidateAddress = candidate.candidateAddress;
            candidates.push(candidateAddress);
        }

        return { totalCandidate, totalVoter, candidates };
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
        return (
            <Layout>
                <h3>Total Candidates: {this.props.totalCandidate}</h3>
                <h3>Total Voter: {this.props.totalVoter}</h3>
                {this.renderCandidates()}
            </Layout>
        );
    };
}

export default ElectionIndex;