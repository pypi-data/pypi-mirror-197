A teeworlds network protocol library, designed according to sans I/O (http://sans-io.readthedocs.io/) principles 

## sample usage

```python
packet = parse(b'\x04\x0a\x00\xcf\x2e\xde\x1d\04') # 0.7 close

print(packet) # => <class: 'TwPacket'>: {'version': '0.7', 'header': <class: 'Header'>, 'messages': [<class: 'CtrlMessage'>]}
print(packet.header) # => <class: 'Header'>: {'flags': <class: 'PacketFlags7, 'size': 0, 'ack': 10, 'token': b'\xcf.\xde\x1d', 'num_chunks': 0}
print(packet.header.flags) # => <class: 'PacketFlags7'>: {'control': True, 'resend': False, 'compression': False, 'connless': False}
for msg in packet.messages:
    print(msg.name) # => close
```

## setup

```bash
git clone https://gitlab.com/teeworlds-network/twnet_parser
cd twnet_parser
python -m venv venv
source venv/bin/activate
pip install -r requirements
```

## tests and linting

```bash
# dev dependencies
pip install -r requirements/dev.txt

# run unit tests
pytest .

# run style linter
pylint src/

# run type checker
mypy src/
```

## package and release

```bash
pip install -r requirements/dev.txt
python -m build
```
