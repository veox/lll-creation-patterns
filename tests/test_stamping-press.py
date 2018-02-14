def get_greeter_addr_from_log(chain, receipt):
    logtopic = receipt['logs'][0]['data']
    assert logtopic != '0x0000000000000000000000000000000000000000000000000000000000000000'

    addr = chain.web3.toChecksumAddress(logtopic)
    return addr

def create_greeter(chain, factory):
    txhash = factory.transact().stamp()
    txreceipt = chain.wait.for_receipt(txhash)

    print(txreceipt) # DEBUG

    greeteraddr = get_greeter_addr_from_log(chain, txreceipt)

    return greeteraddr

########################################################################

def test_press_stamps_greeters(chain):
    sp, _ = chain.provider.get_or_deploy_contract('stamping-press')

    greeter0addr = create_greeter(chain, sp)
    greeter1addr = create_greeter(chain, sp)

    assert greeter0addr != greeter1addr

def test_stamped_greeter(chain):
    sp, _ = chain.provider.get_or_deploy_contract('stamping-press')

    Greeter = chain.provider.get_contract_factory('greeter')
    greeteraddr = create_greeter(chain, sp)
    greeter = Greeter(address=greeteraddr)

    greeting = greeter.call().greet()
    assert greeting == 42

    set_txn_hash = greeter.transact().setGreeting(1337)
    chain.wait.for_receipt(set_txn_hash)

    greeting = greeter.call().greet()
    assert greeting == 1337
