const HDWalletProvider = require('@truffle/hdwallet-provider');
const Web3 = require('web3');
const election = require('./build/Election.json')

const provider = new HDWalletProvider(
    'soft wine toward urban uniform evolve chat enact kick distance fabric front',
    'https://rinkeby.infura.io/v3/446994e58de24ead9539905c5f0059c6'
);

const web3 = new Web3(provider);

const deploy = async () => {
    const accounts = await web3.eth.getAccounts();

    console.log('Attempting to deploy from account:', accounts[0]);

    const result = await new web3.eth.Contract(election.interface)
        .deploy({ data: '0x' + election.bytecode })
        .send({ from: accounts[0], gas: '3000000' });

    console.log('Interface = ', JSON.stringify(election.interface))
    console.log('Contract deployed to', result.options.address);
};

deploy();