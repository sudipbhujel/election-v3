import React from 'react';
import Layout from '../../components/Layout'
import { Card, Divider, Form, Grid, Header, Segment } from 'semantic-ui-react';
import CandidateForm from '../../components/CandidateForm';
import VoterForm from '../../components/VoterForm';
import ElectionControl from '../../components/ElectionControl';

import election from '../../ethereum/election';
import web3 from '../../ethereum/web3';

class Manager extends React.Component {
    state = {
        errorMessage: '',
        loading: false
    };

    static async getInitialProps() {
        let candidates = [];
        const manager = await election.methods.manager().call();
        const accounts = await web3.eth.getAccounts();
        const totalCandidate = await election.methods.totalCandidate().call();
        const totalVoter = await election.methods.totalVoter().call();
        const voteDropped = await election.methods.voteDropped().call();

        for (let i = 0; i < parseInt(totalCandidate); i++) {
            const candidate = await election.methods.candidates(i).call();
            const name = candidate.name;
            const address = candidate.candidateAddress;
            const totalVoteCount = candidate.totalVoteCount;
            candidates.push({ address, name, totalVoteCount });
        }

        return { accounts, manager, totalCandidate, totalVoter, candidates, voteDropped };
    }

    renderCandidates() {
        const items = this.props.candidates.map((candidate, index) => {
            index++;
            return {
                header: candidate.name,
                meta: candidate.address,
                description: `Total Vote: ${candidate.totalVoteCount}`,
                fluid: true,
                style: { overflowWrap: 'break-word' }
            }
        });
        return <Card.Group items={items} />
    }

    render() {
        return (
            <Layout>
                <Segment>
                    <Header as='h3'>Manger Controls</Header>
                    <Divider />
                    <ElectionControl />
                </Segment>
                <h2>Manager: {this.props.manager}</h2>
                <Grid>
                    <Grid.Row>
                        <Grid.Column width={8}>
                            <h3>Candidate</h3>
                            <CandidateForm />
                        </Grid.Column>
                        <Grid.Column width={8}>
                            <h3>Voter</h3>
                            <VoterForm />
                        </Grid.Column>
                    </Grid.Row>
                </Grid>
                <Grid>
                    <Grid.Row>
                        <Grid.Column width={11}>
                            <Segment>
                                <h3>Candidate lists</h3>
                                <Divider />
                                {this.renderCandidates()}
                            </Segment>
                        </Grid.Column>

                        <Grid.Column width={5}>
                            <Segment>
                                <h3>Stats</h3>
                                <Divider />
                                <h4>Total Candidates: {this.props.totalCandidate}</h4>
                                <h4>Total Voter: {this.props.totalVoter}</h4>
                                <h4>Vote Dropped: {this.props.voteDropped}</h4>
                            </Segment>
                        </Grid.Column>
                    </Grid.Row>
                </Grid>
            </Layout>
        );
    }
}

export default Manager;