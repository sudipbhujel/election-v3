import web3 from './web3';
import Election from './build/Election.json';

const instance = new web3.eth.Contract(Election.interface, '0xF1e0afD17a110B3A0d1707D040F23E792a305314');

export default instance;