import sys
sys.path.append('../src/socialism/')

from goddess_service import GoddessService

import asyncio
import random
import aiohttp
import traceback
import uuid

## drawguess
class Drawguess:
    DRAW_CODE = 90001
    GUESS_CODE = 90002
    GIVEUP_CODE = 90003
    
    STATUS_IDLE = 0
    STATUS_DRAWING = 1
    STATUS_GUESSING = 2
    
    def __init__(self, service):
        self.service = service
        
        # self.sd_url = 'https://monitor.lyjzzz.com/'  # lyj的plot，至少不会全是妹子儿
        self.sd_image_url_base = "https://frog.4fun.chat/account/uploads/"
        self.save_path = "/var/www/html/dog-whistle/social-upload/images/"
        # self.sd_url = "https://image1.futuregroups.net/"
        # self.sd_image_url_base = "https://image1.futuregroups.net/maze/"
        
        self.drawguess_status = self.STATUS_IDLE
        self.drawguess_answer = ''
        self.drawguess_times = 0
        self.drawguess_drawer = None
        
        self.service.add_feature('Draw', self.DRAW_CODE, 'draw', self.handle_feature_draw)
        self.service.add_feature('Guess', self.GUESS_CODE, 'guess', self.handle_feature_guess)
        self.service.add_feature('GiveUp', self.GIVEUP_CODE, 'giveup', self.handle_feature_giveup)
    
    def reset_drawguess(self):
        self.drawguess_status = self.STATUS_IDLE
        self.drawguess_answer = ''
        self.drawguess_times = 0
        self.drawguess_drawer = None
    
    async def handle_feature_draw(self, service, data, ws, path):
        if self.drawguess_status == self.STATUS_IDLE:
            self.drawguess_status = self.STATUS_DRAWING
            self.drawguess_drawer = data['extra']['user_id']
            text = data['extra']['draw']
            self.drawguess_answer = text
            channel_id = data['extra']['channel_id']
            try:
                payload = {
                    "prompt": text,
                    "steps": 15
                }
                payload = {
                    "prompt": text,
                    "mode": "fast",
                    "guidance_scale": 5,
                }
                await service.whistle_sender_command_text(
                    data, ws,
                    text_to_sender = f'你要画“{text}”？好啊，等着瞧！\n',
                    text_to_others = f'{data["extra"]["user_id"]}已经选好词儿了，AI正在吭哧瘪肚地画！\n',
                    clear_sender = True,
                    clear_others = True
                )
                async with aiohttp.ClientSession() as session:
                    # f'{self.sd_url}sdapi/v1/txt2img'
                    # lyj是data=payload，我们部署的是json=payload
                    async with session.post("https://monitor.lyjzzz.com/stable_diffusion", data=payload) as resp:
                        content = await resp.read()
                        name = uuid.uuid4()
                        path_to_file = self.save_path + str(name) + '.png'
                        with open(path_to_file, 'wb') as f:
                            f.write(content)
                        img_url = self.sd_image_url_base + str(name) + '.png'
                        # r = await resp.json()
                        # img_url = self.sd_image_url_base + r['img_path']
                        print(img_url)
                        await service.broadcast_command_image(channel_id, ws, img_url)
                        await service.whistle_sender_command_text(
                            data, ws, 
                            text_to_sender = f'好耶！你画的“{text}”已生成喵！等他们猜吧！\n', 
                            text_to_others = f'题目已画好，开始猜吧！提示：长度是{len(text)}噢！\n'
                        )
                        self.drawguess_status = self.STATUS_GUESSING

            except Exception as e:
                traceback.print_exc()
                self.reset_drawguess()
                
        elif self.drawguess_status == self.STATUS_DRAWING:
            await service.reply_command_text(data, ws, '你画我猜已经开始了，AI还在画呢！\n')
        
        elif self.drawguess_status == self.STATUS_GUESSING:
            await service.reply_command_text(data, ws, '你画我猜已经开始了，赶紧切换到Guess那儿去猜！在Draw这发什么癫？\n')
        
        else:
            # 闹鬼了
            pass
        
    async def handle_feature_guess(self, service, data, ws, path):
        if self.drawguess_status == self.STATUS_GUESSING:
            user = data['extra']['user_id']
            if user == self.drawguess_drawer:
                await service.reply_command_text(data, ws, '你画我猜的题目是你自己画的，你猜你自己画的是啥？\n')
            else:
                # 这才判断猜的对不对
                self.drawguess_times += 1
                guess_ans = data['extra']['guess']
                channel_id = data['extra']['channel_id']
                if guess_ans == self.drawguess_answer:
                    # 猜对了
                    # 对猜对回答者
                    await service.reply_command_text(data, ws, f'恭喜你第{self.drawguess_times}次猜对了！答案就是“{self.drawguess_answer}”！\n')
                    # 对出题人
                    # TO DO: 这个接口需要封装
                    await service._send_command_down(
                        ws, 
                        service.codes.COMMAND_DOWN_DISPLAY_TEXT,
                        channel_id = channel_id, 
                        to_user_ids = [self.drawguess_drawer], 
                        args = {'text': f'第{self.drawguess_times}次猜测，{user}猜对了你召唤的画儿！', 'clear': False}
                    )
                    # 对其他回答者
                    await service._send_command_down(
                        ws, 
                        service.codes.COMMAND_DOWN_DISPLAY_TEXT,
                        channel_id = channel_id, 
                        to_user_ids = list(set(service.agent.get_channel_user_list(channel_id)) - {self.drawguess_drawer, user}), 
                        args = {'text': f'第{self.drawguess_times}次猜测，{user}猜对了！答案是{self.drawguess_answer}', 'clear': False}
                    )
                    # 游戏结束
                    self.reset_drawguess()
                else:
                    # 猜错了
                    # 对猜错回答者
                    await service.reply_command_text(data, ws, f'你个憨憨，第{self.drawguess_times}次猜错了！你竟然猜了个{guess_ans}，乐！\n')
                    # 对出题人
                    # TO DO: 这个接口需要封装
                    await service._send_command_down(
                        ws, 
                        service.codes.COMMAND_DOWN_DISPLAY_TEXT,
                        channel_id = channel_id, 
                        to_user_ids = [self.drawguess_drawer], 
                        args = {'text': f'第{self.drawguess_times}次猜测，{user}这个憨憨猜错了！他竟然猜了个{guess_ans}，乐！\n', 'clear': False}
                    )
                    # 对其他回答者
                    await service._send_command_down(
                        ws, 
                        service.codes.COMMAND_DOWN_DISPLAY_TEXT,
                        channel_id = channel_id, 
                        to_user_ids = list(set(service.agent.get_channel_user_list(channel_id)) - {self.drawguess_drawer, user}), 
                        args = {'text': f'第{self.drawguess_times}次猜测，{user}这个憨憨猜错了！他竟然猜了个{guess_ans}，乐！\n', 'clear': False}
                    )
                    
        elif self.drawguess_status == self.STATUS_IDLE:
            await service.reply_command_text(data, ws, '你画我猜还没开始呢，你猜个屁！\n')
        
        elif self.drawguess_status == self.STATUS_DRAWING:
            await service.reply_command_text(data, ws, '正在画画儿呢，你猜个屁！\n')
        
        else:
            # 闹鬼了
            pass
        
    async def handle_feature_giveup(self, service, data, ws, path):
        if self.drawguess_status == self.STATUS_IDLE:
            await service.reply_command_text(data, ws, '你是不是虎？你画我猜还没开始呢，你放弃个屁！\n')
        
        elif self.drawguess_status == self.STATUS_DRAWING:
            await service.reply_command_text(data, ws, '你是不是虎？画儿还没画出来就想放弃？\n')
        
        elif self.drawguess_status == self.STATUS_GUESSING:
            user = data['extra']['user_id']
            if user == self.drawguess_drawer:
                await service.whistle_sender_command_text(
                    data, ws,
                    text_to_sender = f'你放弃了你画的画儿！答案是“{self.drawguess_answer}”！\n',
                    text_to_others = f'您们这群笨蛋！出题人{user}都看不下去了，他活活放弃了！答案是“{self.drawguess_answer}”！\n',
                )
            else:
                channel_id = data['extra']['channel_id']
                # 对放弃者
                await service.reply_command_text(data, ws, f'你猜不出来，放弃了！答案是“{self.drawguess_answer}”！\n')
                # 对出题人
                # TO DO: 这个接口需要封装
                await service._send_command_down(
                    ws, 
                    service.codes.COMMAND_DOWN_DISPLAY_TEXT,
                    channel_id = channel_id, 
                    to_user_ids = [self.drawguess_drawer], 
                    args = {'text': f'你整的太抽象了！{user}猜不出来，放弃了！答案是“{self.drawguess_answer}”！\n', 'clear': False}
                )
                # 对其他回答者
                await service._send_command_down(
                    ws, 
                    service.codes.COMMAND_DOWN_DISPLAY_TEXT,
                    channel_id = channel_id, 
                    to_user_ids = list(set(service.agent.get_channel_user_list(channel_id)) - {self.drawguess_drawer, user}), 
                    args = {'text': f'太抽象了！{user}猜不出来，放弃了！答案是“{self.drawguess_answer}”！\n', 'clear': False}
                )
            # 游戏结束
            self.reset_drawguess()
        else:
            # 闹鬼了
            pass


# websocket.enableTrace(True)
service = GoddessService(
    port = 10003,
    uri = "wss://frog.4fun.chat/badgateway",
    token = "495fc188deff2ff34b0865b0315d329ea33c04bc684b0e4de265f986d7e3826c",
    dbfile = 'test_goddess_db.json',
    name = 'Yellow 502 Goddess Service'
)

drawguess = Drawguess(service)

asyncio.get_event_loop_policy().get_event_loop().run_until_complete(service.get_server_coroutine())
print('----------WRAPPED 502 Goddess Service Starts------------')
asyncio.get_event_loop_policy().get_event_loop().run_forever()
asyncio.ensure_future()