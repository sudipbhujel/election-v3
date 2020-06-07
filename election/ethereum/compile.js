const path = require('path');
const solc = require('solc');
const fs = require('fs-extra');

const buildPath = path.resolve(__dirname, 'build');
fs.removeSync(buildPath);

const electionPath = path.resolve(__dirname, 'contracts', 'Election.sol');
const source = fs.readFileSync(electionPath, 'utf8');

const input = {
    language: 'Solidity',
    sources: {
        'Election.sol' : {
            content: source
        }
    },
    settings: {
        outputSelection: {
            '*': {
                '*': [ '*' ]
            }
        }
    }
}; 

const output = JSON.parse(solc.compile(JSON.stringify(input)));

fs.ensureDirSync(buildPath);

if(output.errors) {
    output.errors.forEach(err => {
        console.log(err.formattedMessage);
    });
} else {
    const contracts = output.contracts["Election.sol"];
    for (let contractName in contracts) {
        const contract = contracts[contractName];
        const { abi: interface, evm: { bytecode: { object } } } = contract;
        fs.writeFileSync(path.resolve(buildPath, `${contractName}.json`), JSON.stringify({interface, bytecode: object}, null, 2), 'utf8');
    }
}