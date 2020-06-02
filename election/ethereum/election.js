import web3 from './web3';
import Election from './build/Election.json';

const instance = new web3.eth.Contract(Election.interface, '0x63E3C6b636FCD8907E0d7cD4C6BaB4d941eD55Ed');

export default instance;