import React from 'react';
import { Form, Input, Button, Message, Icon } from 'semantic-ui-react';
import election from '../ethereum/election';
import web3 from '../ethereum/web3';

class ElectionControl extends React.Component {
    state = {
        errorMessage: '',
        loadingStart: false,
        loaginEnd: false
    };

    onStart = async (event) => {
        event.preventDefault();

        this.setState({ errorMessage: '', loadingStart: true });

        try {
            const accounts = await web3.eth.getAccounts();
            await election.methods.startVote().send({
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
            { value: '', loadingStart: false }
        );
    }

    onEnd = async (event) => {
        event.preventDefault();

        this.setState({ errorMessage: '', loadingEnd: true });

        try {
            const accounts = await web3.eth.getAccounts();
            await election.methods.endVote().send({
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
            { value: '', loadingEnd: false }
        );
    }

    renderMessage() {
        if (this.state.errorMessage.length != 0) {
            return <Message error header="Oops" content={this.state.errorMessage} />
        }
    }

    render() {
        return (
            <div>
                <Button onClick={this.onStart} primary content='Start Vote' icon='play circle outline' labelPosition='right' loading={this.state.loadingStart} />
                <Button onClick={this.onEnd} color='red' content='End Vote' icon='stop circle outline' labelPosition='right' loading={this.state.loadingEnd} />
                {this.renderMessage()}
            </div>
        )
    }
}

export default ElectionControl;