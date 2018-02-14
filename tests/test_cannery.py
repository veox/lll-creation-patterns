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

    print(txhash)    # DEBUG
    print(txreceipt) # DEBUG
    print('-'*72)

    # get can's address from log
    assert len(txreceipt['logs']) != 0
    canaddr = chain.web3.toChecksumAddress(txreceipt['logs'][0]['data'])
    assert canaddr != '0x0000000000000000000000000000000000000000'

    # see what's in the can (cheat!)
    canbytecode = chain.web3.eth.getCode(canaddr)
    print('can bytecode:', canbytecode)
    print('-'*72)

    # attempt to call can directly (should fail)
    transaction = {
        'from': chain.web3.eth.coinbase,
        'to':   canaddr,
        'gas': 42000
    }
    txhash = chain.web3.eth.sendTransaction(transaction)
    txreceipt = chain.wait.for_receipt(txhash)

    print(txhash)    # DEBUG
    print(txreceipt) # DEBUG
    
    assert False
