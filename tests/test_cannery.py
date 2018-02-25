import pytest
from ethereum.tester import TransactionFailed

# bytecode of *revert-guard* in cannery/can-opener contracts
revertguard = '0x600080fd' # PUSH1 0x00 DUP1 REVERT

def _print_memdump(chain, txreceipt):
    '''Hacky helper for memory inspection.'''
    print('-'*33 + 'MEMDMP' + '-'*33)
    data = txreceipt['logs'][0]['data']
    data = data[2:] # snip 0x
    for i in range(int(len(data)/64)):
        print(chain.web3.toHex(i*32), data[i*64:i*64+64], sep='\t')

    # FIXME: required since accessing logs by index instead of event id;
    # also, forces the dump to be displayed
    assert False

def _get_log_data(txreceipt, logindex=0):
    '''Extract ``data`` from log entry in the transaction receipt.'''
    assert len(txreceipt['logs']) != 0
    return txreceipt['logs'][logindex]['data']

def can_contract(chain, cannery, contractname):
    factory = chain.provider.get_contract_factory(contractname)
    transaction = {
        'from': chain.web3.eth.coinbase,
        'to':   cannery.address,
        'data': factory.bytecode,
    }
    txhash = chain.web3.eth.sendTransaction(transaction)
    txreceipt = chain.wait.for_receipt(txhash)

    # get can's address from log
    canaddr = chain.web3.toChecksumAddress(_get_log_data(txreceipt))
    assert canaddr != '0x0000000000000000000000000000000000000000'

    return canaddr

def open_canned_contract(chain, opener, canaddr, data=None):
    # open the canned vegetable using the can-opener
    if data is None:
        txhash = opener.transact().open(canaddr)
    else:
        txhash = opener.transact().open(canaddr, data)
    txreceipt = chain.wait.for_receipt(txhash)

    # # DEBUG (uncomment here and in contract!)
    # _print_memdump(chain, txreceipt)

    # get uncanned contract's address from log
    openedaddr = chain.web3.toChecksumAddress(_get_log_data(txreceipt))
    assert openedaddr != '0x0000000000000000000000000000000000000000'

    return openedaddr

def deploy_cannery_and_can(chain):
    # deploy cannery
    cannery, _ = chain.provider.get_or_deploy_contract('cannery')

    # construct a transaction that has a veggie's deployment code,
    # but send it to the cannery instead of a direct CREATE
    Vegetable = chain.provider.get_contract_factory('vegetable')

    canaddr = can_contract(chain, cannery, 'vegetable')

    # see what's in the can (cheat!)
    canbytecode = chain.web3.eth.getCode(canaddr)
    # "normal" runtime bytecode is in the can (remove leading '0x's)
    assert Vegetable.bytecode[2:] in canbytecode[2:]
    # the can has a revert guard
    assert canbytecode.startswith(revertguard)
    # there is nothing else but the can and its contents
    assert canbytecode == revertguard + Vegetable.bytecode[2:]

    # attempt calling can directly (should REVERT with very low gas use)
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

    return (cannery, canaddr)

########################################################################

def test_cannery(chain):
    deploy_cannery_and_can(chain)

def test_can_opener_without_data(chain):
    # deploy cannery and canned vegetable
    cannery, canaddr = deploy_cannery_and_can(chain)
    # deploy can opener
    opener, _ = chain.provider.get_or_deploy_contract('can-opener')

    # try opening the can
    Vegetable = chain.provider.get_contract_factory('vegetable')
    veg1addr = open_canned_contract(chain, opener, canaddr)
    veg1 = Vegetable(address=veg1addr)

    # uncanned vegetable's runtime bytecode matches that of never-canned
    assert chain.web3.eth.getCode(veg1addr) == Vegetable.bytecode_runtime

    # try calling it (using "fake" function, since Populus no-know "fallbacks")
    retval = veg1.call().fake()
    # is 0x0000000000000000000000000000000000000000000000000000000000000000
    assert chain.web3.toHex(retval) == '0x'+'0'*64

def test_can_opener_with_data(chain):
    # will use this "fingerprint"
    somebytes = chain.web3.toBytes(0xfacade)

    # deploy cannery and canned vegetable
    cannery, canaddr = deploy_cannery_and_can(chain)
    # deploy can opener
    opener, _ = chain.provider.get_or_deploy_contract('can-opener')

    # try opening the can
    Vegetable = chain.provider.get_contract_factory('vegetable')
    veg2addr = open_canned_contract(chain, opener, canaddr, data=somebytes)
    veg2 = Vegetable(address=veg2addr)

    # uncanned vegetable's runtime bytecode matches that of never-canned
    assert chain.web3.eth.getCode(veg2addr) == Vegetable.bytecode_runtime

    # try calling it (using "fake" function, since Populus no-know "fallbacks")
    retval = veg2.call().fake()
    retval = retval.encode('latin-1') # UGLY: Populus/web3 quirk
    # is 0xfacade0000000000000000000000000000000000000000000000000000000000
    assert retval.startswith(somebytes)
