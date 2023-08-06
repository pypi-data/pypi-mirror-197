# SIMSIMI
![api logo](https://raw.githubusercontent.com/AKXVAU/simipro/main/assets/logo.png)
> [Simsimi](https://github.com/AKXVAU/simsimi) API in Python.
> ![pypi](https://img.shields.io/pypi/v/simipro?logo=python)

## Description
World first popular Chatbot for daily conversation (Service launched in 2002). A unique daily conversation with diversity, fun and vitality. Service provided with 130 million sets of daily small talks in 81 languages compiled through more than 20 million panels. Service in 81 languages. More than 350 million cumulative users worldwide. (Based on June-2018), Records of more than 200 million times of responses made per day.

#### REQUIREMENTS
* `PYTHON >=3.9.X+`
* `REQUESTS`

#### Installation 
```bash
pip3 install simipro
```
#### Or
```bash
pip install -i https://test.pypi.org/simple/ simipro
```
## SimiTalk
#### Import Module
```python
from simipro import simiTalk
```
#### Use SimSimi talk function
```python
from simipro import simiTalk
req = simiTalk ("hi", "en")
print (req)
```
#### Response
```json
{
    "status": "true",
    "time": "06:55:47 PM",
    "type": "text",
    "lc": "en",
    "ans": "Hello back",
    "author": "𝙷𝙰𝚇𝙾𝚁 𝚇𝙽𝚇",
    "owner" : "https://t.me/haxor_xnx",
    "channel" : "https://t.me/Toxinum"
}
```
#### Realtime Example for SimSimi talk
```python 
from simipro import simiTalk
msg = "hi"
lang = "en"
req = simiTalk (msg, lang)
print (req["ans"])
```
#### Response
```bash
Hello there
```
## SimiTeach
#### Import Module
```python
from simipro import simiTeach
```
#### Use SimSimi teach function
```python
from simipro import simiTeach
req = simiTeach ("hi" ,"hello, "en", "YOUR_SECRET_KEY")
print (req)
```
#### Response
```json
{
    "status": "true",
    "time": "06:55:47 PM",
    "type": "text",
    "lc": "en",
    "ask": "hello world",
    "ans": "Hello back",
    "author": "𝙷𝙰𝚇𝙾𝚁 𝚇𝙽𝚇",
    "owner" : "https://t.me/haxor_xnx",
    "channel" : "https://t.me/Toxinum"
}
```
#### Realtime Example for SimSimi teach
```python
from simipro import simiTeach
msgAsk = "hi"
msgAns = "hello"
lang = "en"
secretKey = "YOUR_SECRET_KEY"
req = simiTeach (msgAsk, msgAns, lang, secretKey)
print (req["ask"])
print (req["ans"])
```
#### Response
```bash
hi
hello
```
## License 
MIT License

Copyright (c) 2023 Mohammad Alamin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

> Build with [Simsimi](https://simsimi.com/) official api.

#### Open Source Project.

### Contact With Developer
<hr>
<div align="center">
<a href="https://facebook.com/AKXVAU" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/facebook.svg" alt="itsn0b1t4" height="30" width="40" /></a>
<a href="https://instagram.com/AKXVAU" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="itsn0b1t4" height="30" width="40" /></a>
<a href="https://www.youtube.com/c/akxvau" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/youtube.svg" alt="akxvau" height="30" width="40" /></a>
</p>
<hr>
</div>