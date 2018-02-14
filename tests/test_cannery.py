import pytest
from ethereum.tester import TransactionFailed

def print_memdump(chain, txreceipt):
    print('-'*33 + 'MEMDMP' + '-'*33)
    data = txreceipt['logs'][0]['data']
    data = data[2:] # snip 0x
    for i in range(int(len(data)/64)):
        print(chain.web3.toHex(i*32), data[i*64:i*64+64], sep='\t')

    # FIXME: required since accessing logs by index instead of event id
    assert False

########################################################################

def test_cannery(chain):
    # deploy cannery and can opener
    cannery, _ = chain.provider.get_or_deploy_contract('cannery')
    opener, _ = chain.provider.get_or_deploy_contract('can-opener')

    # construct a transaction that has a veggie's deployment code,
    # but send it to the cannery instead of a direct CREATE
    Vegetable = chain.provider.get_contract_factory('vegetable')
    bytecode = Vegetable.bytecode
    transaction = {
        'from': chain.web3.eth.coinbase,
        'to':   cannery.address,
        'data': bytecode,
    }
    txhash = chain.web3.eth.sendTransaction(transaction)
    txreceipt = chain.wait.for_receipt(txhash)

    # print_memdump(chain, txreceipt) # DEBUG (uncomment here and in contract!)

    # DEBUG
    print('transaction:', transaction)
    print(txhash)
    print(txreceipt)
    print('-'*72)

    # get can's address from log
    assert len(txreceipt['logs']) != 0
    canaddr = chain.web3.toChecksumAddress(txreceipt['logs'][0]['data'])
    assert canaddr != '0x0000000000000000000000000000000000000000'

    # see what's in the can (cheat!)
    canbytecode = chain.web3.eth.getCode(canaddr)
    revertguard = '0x600080fd'
    # "normal" runtime bytecode is in the can
    assert bytecode[2:] in canbytecode[2:]
    # the can has a revert guard
    assert canbytecode.startswith(revertguard)
    # there is nothing else but the can and its contents
    assert canbytecode == revertguard + bytecode[2:]

    # DEBUG
    print('can', canaddr, 'bytecode:')
    print(canbytecode)
    print('-'*72)

    # attempt to call can directly (should REVERT with very low gas use)
    transaction = {
        'from': chain.web3.eth.coinbase,
        'to':   canaddr,
        'gas': 100000, # TODO: this seems not to be used?.. :/
    }
    with pytest.raises(TransactionFailed):
        txhash = chain.web3.eth.sendTransaction(transaction)
    txreceipt = chain.wait.for_receipt(txhash)
    # FIXME: Populus uses an ancient version of `pyethereum`; looks like
    # it doesn't know of REVERT and its reduced gas use
    #assert txreceipt['gasUsed'] < 21100

    # DEBUG
    print('transaction:', transaction)
    print(txhash)
    print(txreceipt)
    
    assert False
