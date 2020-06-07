import React from 'react';
import election from '../ethereum/election';
import Layout from '../components/Layout';
import { Button, Card, Message } from 'semantic-ui-react';
import web3 from '../ethereum/web3';
import { totalCandidate, totalVoter, voteDropped } from '../ethereum/stats'

import { Link } from '../routes';

class ElectionIndex extends React.Component {
    state = {
        errorMessage: '',
        loading: false
    }
    static async getInitialProps() {
        let candidates = [];
        const manager = await election.methods.manager().call();
        const totalCandidate = await election.methods.totalCandidate().call();
        const totalVoter = await election.methods.totalVoter().call();
        const voteDropped = await election.methods.voteDropped().call();

        for (let i = 0; i < parseInt(totalCandidate); i++) {
            const candidate = await election.methods.candidates(i).call();
            const name = candidate.name;
            const address = candidate.candidateAddress;
            candidates.push({address, name});
        }

        return { manager, totalCandidate, totalVoter, candidates, voteDropped };
    }

    onVote = async (event) => {
        event.preventDefault();
        this.setState({ errorMessage: '', loading: true });

        const index = event.target.value - 1;
        try {
            const accounts = await web3.eth.getAccounts();
            await election.methods.doVote(parseInt(index)).send({
                from: accounts[0],
                gas: '1000000'
            });
            console.log('voted to', index);
            // Router.replaceRoute(`/campaigns/${this.props.address}`);
        } catch (error) {
            this.setState(
                { errorMessage: error.message }
            );
        };

        this.setState(
            { value: '', loading: false }
        );
    }

    renderCandidates() {
        const items = this.props.candidates.map((candidate, index) => {
            index++;
            return {
                header: candidate.name,
                meta: candidate.address,
                // fluid: true,
                extra: <Button key={index} onClick={this.onVote} value={index} loading={this.state.loading} inverted primary>Vote</Button>,
                style: { overflowWrap: 'break-word' }
            }
        });
        return <Card.Group items={items} />
    }

    renderMessage(){
        if (this.state.errorMessage.length != 0){
            return <Message error header="Oops" content={this.state.errorMessage}/>
        }
    }

    render() {
        return (
            <Layout>
                {this.renderMessage()}
                <h3>Candidates</h3>
                {this.renderCandidates()}
            </Layout>
        );
    };
}

export default ElectionIndex;