# message-queue

In a parent directory run

```bash
pip install mq_sa 
```

Create interprocess message queue and send 

```python
import mq_sa
q=mq_sa.create('myqueue', 100)
mq_sa.send(q, 'fo', 'bar', 'baz', 'quux')
```

Receive like this 

```python
import mq_sa
q=mq_sa.open('myqueue')
mq_sa.receive(q)
('fo', 'bar', 'baz', 'quux')
```

## Release new version

Bump version in `setup.py` and 

```
rm -rf dist/ && \
python setup.py sdist && \
twine upload dist/* -usmashingalpha -p`cat .env | grep TWINE_PASSWORD | cut -d '=' -f 2- | tr -d '"'`
```

## Boost install directory and Pyenv 

If boost installed in eg `$HOME/boost` then, why - https://github.com/scikit-build/scikit-build/issues/733

```bash
export SKBUILD_CONFIGURE_OPTIONS="-DBOOST_ROOT=$HOME/boost" && \
pip install mq_sa 
```

And copy boost python to where Python can find it with its @rpath like this 

```bash
cp $HOME/boost/lib/libboost_python311.* $HOME/.pyenv/versions/3.11.2/lib
```
