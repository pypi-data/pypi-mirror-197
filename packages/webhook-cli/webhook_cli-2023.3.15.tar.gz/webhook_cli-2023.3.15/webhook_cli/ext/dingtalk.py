#!python3
### 配置默认使用 config.toml  
### 钉钉 https://open.dingtalk.com/document/robots/custom-robot-access
### 

import os
import json
import datetime
import shutil
from pprint import pprint
from collections import OrderedDict

import pyco_utils
import requests
import rtoml
import json5

from pyco_utils._json import pformat_json
from pyco_utils.co_shutil import safely_open
from webhook_cli._helper import env, env_bool, BColors


class WebhookDingTalk():
    cfg_dir = os.environ.get("HOME", os.getcwd())
    cfg_system = os.path.join(cfg_dir, ".config/webhook_cli/config.toml")
    cfg_default = os.path.join(os.getcwd(), "config.toml")
    cfg_custom = ""
    desc = "[配置优先级]：${config} >  ENV.$WEBHOOK_CONFIG   > config.toml > $HOME/.config/webhook_cli/config.toml"

    _options_sample_ = dict(
        app_type="dingtalk",
        app_desc="\n钉钉群机器人配置模板（可设置为 ENV.$WEBHOOK_CONFIG , 支持toml/json）："
                 "\n 0. webhook_url 必要的配置项, 其它均为可选；"
                 "\n 1. 以`x`前缀的配置项, 是内置的控制项；"
                 "\n 2. 以`_`前缀的配置项, 是开发调试参数, 不建议稳定版本使用；"
                 "\n 3. 以`#`前缀或后缀的配置项, 可视为注释，可忽略；"
                 "\n 4. 其它参数与 app_type (默认为'dingtalk')相关, 不一而论。"
                 "\n\n",
        keyword="webhook通知的关键词",
        webhook_url="https://oapi.dingtalk.com/robot/send?access_token=${}",
        at_mobiles=["${手机号码1}", "${手机号码2}"],
        at_mobiles_global=[],
        x_cached_msg_dir="./_.webhook-cached",
        x_cached_msg_always=False,
        x_cached_msg_if_failed=True,
    )
    _options_sample_["_ENV_PARAM_REFER_MAP_"] = dict(
        WEBHOOK_URL="自定义url",
        WEBHOOK_CONFIG="自定义配置文件",
    )


    @classmethod
    def get_config_file(cls, nullable=True):
        if cls.cfg_custom:
            if not os.path.isfile(cls.cfg_custom):
                print(f"[配置文件不存在] 请检查路径 {cls.cfg_custom} (cwd: {os.getcwd()})")
                if not nullable:
                    raise FileNotFoundError(cls.cfg_custom)
                else:
                    return None
            else:
                print(f"[自定义配置] {cls.cfg_custom} ")
                return cls.cfg_custom

        config_file = env("WEBHOOK_CONFIG", cls.cfg_default)
        if os.path.exists(config_file):
            print(f"[使用配置] {config_file} ")
            return config_file
        elif config_file != cls.cfg_default:
            print(f"[配置无效] 找不到此文件( ENV.$WEBHOOK_CONFIG  ): {config_file} ")
            if not nullable:
                raise FileNotFoundError(config_file)
        elif os.path.exists(cls.cfg_system):
            print(f"[系统配置] {cls.cfg_system} ")
            return cls.cfg_system

        print(f"[配置失效] webhook_cli 找不到配置文件 !!!")
        if not nullable:
            print(cls.desc)
            raise FileNotFoundError(cls.cfg_default)


    @classmethod
    def get_config_options(cls, stdout=False, **kwargs):
        if stdout:
            print(cls.desc)
            print(f"[系统配置]:{cls.cfg_system}  ({os.path.exists(cls.cfg_system)})")
            print(f"[缺省配置]:{cls.cfg_default} ({os.path.exists(cls.cfg_default)})", )

        fp = cls.get_config_file(nullable=True)
        if fp is None:
            return kwargs

        if fp.endswith(".json") or fp.endswith(".json5"):
            with open(fp, "r") as fr:
                data = json5.load(fr)  # type:dict
                data.update(kwargs)
        else:
            with open(fp, "r") as fr:
                data = rtoml.load(fr)
                data.update(kwargs)
        if stdout:
            text = rtoml.dumps(data, pretty=True)
            print("\n" + "##" * 20 + BColors.OK)
            print(text)
            print(BColors.ENDC + "##" * 20 + "\n")
        webhook_url = data.get("webhook_url")
        if not webhook_url:
            print(f"[当前配置] {fp}\n")
            print("[该配置无效] 必须提供有效的$webhook_url")
            cls.set_config_sample(output_file="")
        return data


    @classmethod
    def set_config_sample(cls, output_file: (str, bool) = cfg_default, **kwargs):
        output_rel = os.path.relpath(output_file, os.getcwd())
        print("\n" + "##" * 20)
        print(f"## 生成参考配置: {output_rel} " + BColors.OK)
        options = cls._options_sample_
        text = rtoml.dumps(options, pretty=True)
        print(text)
        print(BColors.ENDC + "##" * 20 + "\n")
        if output_file and isinstance(output_file, str):
            if os.path.exists(output_file):
                print(f"[配置文件已存在] {output_file}")
                print(f"[建议] 如果要覆盖配置, 先备份再删除, 然后重试。")
            else:
                with safely_open(output_file, "w") as fo:
                    fo.write(text)
                print(f"[配置文件已保存] {output_rel}")
        return options

    @classmethod
    def _send_data(cls, msgtype: str, msgdata: dict, is_at_all=False, **kwargs):
        options = cls.get_config_options(**kwargs)
        at_mobiles = options.get("at_mobiles", [])
        at_mobiles_g = options.get("at_mobiles_global", [])
        at_mobiles.extend(at_mobiles_g)

        webhook_url = options.get("webhook_url")
        keyword = options.get("keyword", "")

        data = dict(
            msgtype=msgtype,
            at=dict(
                atMobiles=at_mobiles,
                isAtAll=is_at_all,
                # atUserIds=["user123"],
            )
        )
        data[msgtype] = msgdata
        if not webhook_url:
            print("[通知失败] invalid $webhook_url")
            pprint(msgdata, indent=2)
            return -1, data

        now = datetime.datetime.now()
        resp = requests.post(webhook_url, json=data)
        if resp.status_code == 200:
            print(f"[发送通知] {keyword} {msgtype} at_mobiles:{at_mobiles}")
            resp_data = resp.json()  # type:dict
            print("[response]", resp_data)
            errcode = resp_data.get("errcode")
            data = OrderedDict(
                webhook="dingtalk",
                msgtype=msgtype,
                msgdata=msgdata,
                options=options,
                _debug_info=dict(
                    now=now,
                    response=resp_data,
                    webhook_url=webhook_url,
                ),
            )

            # post_text = pformat_json(data)
            post_text = rtoml.dumps(dict(data), pretty=True)
            post_md5 = pyco_utils.md5sum((post_text))[:6]

            is_cached = options.get("x_cached_msg_always", False)
            if errcode > 0:
                print("[发送失败]", pformat_json(post_text))
                if options.get("x_cached_msg_if_failed", True):
                    is_cached = True

            if is_cached:
                cached_dir = options.get("x_cached_msg_dir", "_.webhook-cached")
                now_str = now.strftime("%y%m%d_%H%M")
                fn = f'msg_{now_str}_{msgtype}.{post_md5}.toml'
                fout = os.path.join(cached_dir, fn)
                with safely_open(fout, "w") as fo:
                    fo.write(post_text)

            return errcode, resp
        else:
            print(f"[发送异常] {keyword} {msgtype} {at_mobiles}")
            pprint(msgdata, indent=2)
            return 1, resp


    @classmethod
    def send(cls, data: dict, **kws):
        if isinstance(data, str):
            return cls.send_text(data)

        if not isinstance(data, dict):
            print("参数异常")
            return -4, data

        msgtype = data.get("msgtype", "text")
        msgdata = data.get("msgdata", None)
        options = data.get("options", kws)
        if isinstance(msgdata, dict):
            print(f"get msgtype={msgtype}")
            return cls._send_data(msgtype, msgdata, **options)
        else:
            func = getattr(cls, f"send_{msgtype}".lower(), None)
            if callable(func):
                print(f"get msgtype={msgtype}")
                return func(**data)
            else:
                print(f"invalid msgtype={msgtype}")
                return -5, data

    @classmethod
    def send_file(cls, msg_file, **kwargs):
        config_options = cls.get_config_options(**kwargs)

        if not os.path.exists(msg_file):
            print(f"参数异常，文件不存在(task_file={msg_file})")
            return -1, msg_file

        with open(msg_file, "r") as fr:
            keyword = config_options.get("keyword", "WEBHOOK-通知")
            text = fr.read()
            if msg_file.lower().endswith(".toml"):
                data = rtoml.loads(text)
            elif msg_file.lower().endswith(".json"):
                data = json.loads(text)
            elif msg_file.lower().endswith(".md"):
                data = dict(
                    msgtype="markdown",
                    msgdata=dict(
                        title=f"[{keyword}] {os.path.basename(msg_file)}",
                        text=text
                    )
                )
            else:
                data = dict(
                    msgtype="text",
                    msgdata=dict(content=f"[{keyword}]{text}"),
                    options=config_options,
                )

            if (not isinstance(data, dict)) or (data.get("msgtype") is None):
                # content = rtoml.dumps(data, pretty=True)
                data = dict(
                    msgtype="markdown",
                    msgdata=dict(
                        title=f"[{keyword}] {os.path.basename(msg_file)}",
                        text=f"\n```\n{text}\n```\n"
                    ),
                    options=config_options,
                )

            code, resp = cls.send(data, **config_options)
            return code

    @classmethod
    def send_text(cls, content, **kwargs):
        """
        {
            "at": {
                "atMobiles":[
                    "180xxxxxx"
                ],
                "atUserIds":[
                    "user123"
                ],
                "isAtAll": false
            },
            "text": {
                "content":"我就是我, @XXX 是不一样的烟火"
            },
            "msgtype":"text"
        }
        """
        msgtype = "text"
        msgdata = dict(content=content)
        code, resp = cls._send_data(msgtype, msgdata, **kwargs)
        return code, resp

    @classmethod
    def send_link(cls, title="", text="", picUrl="", msgUrl="", **kwargs):
        """
        {
            "msgtype": "link",
            "link": {
                "text": "消息内容。如果太长只会部分展示",
                "title": "消息标题",
                "picUrl": "图片URL",
                "messageUrl": "点击消息跳转的URL"
            }
        }
        """
        msgtype = "link"
        msgdata = dict(title=title, text=text, picUrl=picUrl, messageUrl=msgUrl)
        code, resp = cls._send_data(msgtype, msgdata, **kwargs)
        return code, resp

    @classmethod
    def send_markdown(cls, title="", text="", **kwargs):
        msgtype = "markdown"
        msgdata = dict(title=title, text=text)
        code, resp = cls._send_data(msgtype, msgdata, **kwargs)
        return code, resp

    @classmethod
    def send_actioncard(cls, title="", text="", singleTitle="", singleURL="", btnOrientation=0, **kwargs):
        msgtype = "actionCard"
        btns = kwargs.pop("btns", [])
        if len(btns) > 0:
            msgdata = dict(
                text=text,
                title=title,
                btnOrientation=btnOrientation,
                btns=btns,
            )
        elif singleURL and singleTitle:
            msgdata = dict(
                text=text,
                title=title,
                singleURL=singleURL,
                singleTitle=singleTitle,
                btnOrientation=btnOrientation,
            )
        else:
            print(f"[invalid] $msgtype={msgtype}")
            data = locals().copy()
            pprint(data, indent=2)
            return -2, data

        code, resp = cls._send_data(msgtype, msgdata, **kwargs)
        return code, resp

    @classmethod
    def send_feedcard(cls, links: list, **kwargs):
        """
        {
            "msgtype":"feedCard",
            "feedCard": {
                "links": [
                    {
                        "title": "时代的火车向前开1", 
                        "messageURL": "https://www.dingtalk.com/", 
                        "picURL": "https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png"
                    },
                    {
                        "title": "时代的火车向前开2", 
                        "messageURL": "https://www.dingtalk.com/", 
                        "picURL": "https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png"
                    }
                ]
            }
        }
        """
        msgtype = "feedCard"
        msgdata = dict(links=links)
        code, resp = cls._send_data(msgtype, msgdata, **kwargs)
        return code, resp
