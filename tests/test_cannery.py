import pytest
from ethereum.tester import TransactionFailed

# bytecode of *revert-guard* in cannery/can-opener contracts
revertguard = '0x600080fd' # PUSH1 0x00 DUP1 REVERT

def print_memdump(chain, txreceipt):
    '''Hacky helper for memory inspection.'''
    print('-'*33 + 'MEMDMP' + '-'*33)
    data = txreceipt['logs'][0]['data']
    data = data[2:] # snip 0x
    for i in range(int(len(data)/64)):
        print(chain.web3.toHex(i*32), data[i*64:i*64+64], sep='\t')

    # FIXME: required since accessing logs by index instead of event id;
    # also, forces the dump to be displayed
    assert False

def get_log_data(txreceipt, logindex=0):
    '''Extract ``data`` from log entry in the transaction receipt.'''
    assert len(txreceipt['logs']) != 0
    return txreceipt['logs'][logindex]['data']

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

    # get can's address from log
    canaddr = chain.web3.toChecksumAddress(get_log_data(txreceipt))
    assert canaddr != '0x0000000000000000000000000000000000000000'

    # see what's in the can (cheat!)
    canbytecode = chain.web3.eth.getCode(canaddr)
    # "normal" runtime bytecode is in the can (remove leading '0x's)
    assert bytecode[2:] in canbytecode[2:]
    # the can has a revert guard
    assert canbytecode.startswith(revertguard)
    # there is nothing else but the can and its contents
    assert canbytecode == revertguard + bytecode[2:]

    # attempt to call can directly (should REVERT with very low gas use)
    transaction = {
        'from': chain.web3.eth.coinbase,
        'to':   canaddr,
        'gas': 100000, # TODO: this seems not to be used?.. :/
    }
    # FIXME: .raises() required due to exceptional termination
    with pytest.raises(TransactionFailed):
        txhash = chain.web3.eth.sendTransaction(transaction)
    txreceipt = chain.wait.for_receipt(txhash)
    # FIXME: Populus uses an ancient version of `pyethereum` for testing?..
    # looks like it doesn't know of REVERT, so terminates as if INVALID was called
    #assert txreceipt['gasUsed'] < 21100

    # open the canned vegetable using the can-opener
    txhash = opener.transact().open(canaddr)
    txreceipt = chain.wait.for_receipt(txhash)

    # DEBUG (uncomment here and in contract!)
    # print_memdump(chain, txreceipt)

    # get uncanned contract's address from log
    myveggieaddr = chain.web3.toChecksumAddress(get_log_data(txreceipt))
    assert myveggieaddr != '0x0000000000000000000000000000000000000000'

    # see what's in the veggie (cheat!)
    myveggiebytecode = chain.web3.eth.getCode(myveggieaddr)
    # uncanned vegetable's runtime bytecode matches that of never-canned
    assert myveggiebytecode == Vegetable.bytecode_runtime

    myveggie = Vegetable(address=myveggieaddr)

    # try calling it
    retval = myveggie.call().fake()

    # DEBUG
    print('retval:', chain.web3.toHex(retval))

    assert False

    # TODO: test opening can with data!
