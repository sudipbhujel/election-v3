import Web3 from 'web3';

let web3 = new Web3();
let provider;

if (typeof window !== 'undefined' && typeof window.web3 !== 'undefined') {
    // We are in the browser and metamask is running.
   provider = Web3.givenProvider;
   console.log('Using Metamask')
} else {
    // We are on the sever OR the user is not running metamask
    provider = new Web3.providers.HttpProvider(
        'https://rinkeby.infura.io/v3/446994e58de24ead9539905c5f0059c6'
    );
	console.log('Using Metamask')
}

web3.setProvider(provider);

export default web3;