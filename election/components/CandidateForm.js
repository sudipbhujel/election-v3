import React from 'react';
import { Form, Input, Button, Message, Icon } from 'semantic-ui-react';
import election from '../ethereum/election';
import web3 from '../ethereum/web3';

class CandidateForm extends React.Component {
    state = {
        value: '',
        errorMessage: '',
        loading: false
    };

    onSubmit = async (event) => {
        event.preventDefault();

        this.setState({ errorMessage: '', loading: true });

        try {
            const accounts = await web3.eth.getAccounts();
            await election.methods.addCandidate(this.state.value).send({
                from: accounts[0],
                gas: '1000000'
            });
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

    render() {
        return (
            <Form onSubmit={this.onSubmit} error={!!this.state.errorMessage}>
                <Form.Field>
                    <label>Candidate Address</label>
                    <Input
                        value={this.state.value}
                        onChange={event => this.setState({ value: event.target.value })}
                        label="address"
                        labelPosition="right"
                    />
                </Form.Field>
                <Message error header="Oops!" content={this.state.errorMessage} />
                <Button primary content='Add Candidate' icon='add' labelPosition='right' loading={this.state.loading}/>
            </Form>
        )
    }
}

export default CandidateForm;