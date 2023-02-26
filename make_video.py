import cv2
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from PIL import ImageFont, ImageDraw, Image, ImageOps
import os
import re

# tạo main
def main():
    # Kích thước khung hình của video
    width_frame = 1920
    height_frame = 1080

    # Số khung hình trên giây của video
    fps = 1

    # Vị trí bắt đầu của vùng hiển thị nội dung tin nhắn
    msg_start_x = 350
    msg_start_y = 250

    # khoảng cách giữa các dòng tin nhắn
    msg_line_spacing = 100

    # Khoảng cách các đoạn chat
    msg_spacing = 200

    frame = 255 * np.ones((height_frame, width_frame, 3), dtype=np.uint8)
    # set background
    background = cv2.imread('asset/background2.jpg')
    background = cv2.resize(background, (width_frame, height_frame))

    # Xác định font chữ và kích thước của tin nhắn
    fontpath = "asset\Tahoma Regular font.ttf"     
    font = ImageFont.truetype(fontpath, 80)
    def insert_image(background, image, x, y):
        # add image to frame
        img_pil = Image.fromarray(background)
        img_pil_insert = Image.fromarray(image)
        img_pil.paste(img_pil_insert, (x, y))
        background = np.array(img_pil)
        return background

    def avt_draw(background, image, x, y):
        # Tạo ảnh mới để vẽ hình tròn
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, image.size[0], image.size[1]), fill=255)

        # Áp dụng mask để bo tròn ảnh
        rounded_image = Image.new("RGBA", image.size, 0)
        rounded_image.paste(image, (0, 0), mask=mask)

        # Tính toán vị trí để ghép ảnh bo tròn lên ảnh background
        x_offset = x
        y_offset = y

        # Ghép ảnh bo tròn lên ảnh background
        background.paste(rounded_image, (x_offset, y_offset), rounded_image)
        background = np.array(background)
        return background

    def frame_chat(background, x, y, len_mess, line, type = 0):
        img_pil = Image.fromarray(background)
        background = img_pil
        if line > 5:
            line = 5
        # Đọc ảnh khung chat
        if type == 0:
            foreground2 = Image.open("asset/1 den''.png")
            if line == 1:
                # Đọc ảnh nền và ảnh dán
                foreground1 = Image.open("asset/" + str(line)+" den.png")
                foreground3 = Image.open("asset/" + str(line)+" den'''.png")
            else:
                foreground1 = Image.open("asset/" + str(line)+" den.png")
                foreground3 = Image.open("asset/" + str(line)+" den'.png")
        else:
            foreground2 = Image.open("asset/1 di''.png")
            if line == 1:
                # Đọc ảnh nền và ảnh dán
                foreground3 = Image.open("asset/" + str(line)+" di.png")
                foreground1 = Image.open("asset/" + str(line)+" di'''.png")
            else:
                foreground3 = Image.open("asset/" + str(line)+" di.png")
                foreground1 = Image.open("asset/" + str(line)+" di'.png")

        if line == 1:
            # get size of foreground1
            new_size = (300, 300)
            # dán đầu
            foreground = foreground1.resize(new_size)
            r, g, b, a = foreground.split()
            foreground = Image.merge("RGBA", (b, g, r, a))

            # Dán ảnh dán vào vị trí position trên ảnh nền
            position = (x, y)
            background.paste(foreground, position, foreground)
            # ----------------------------------------------------------
            # dán giữa
            position = (x + 300, y)
            if len_mess > 300:
                new_size_ = (len_mess-300, 300)
            else:
                new_size_ = (5, 300)
            foreground = foreground2.resize(new_size_)
            r, g, b, a = foreground.split()
            foreground = Image.merge("RGBA", (b, g, r, a))
            if len_mess > 200:
                # Dán ảnh dán vào vị trí position trên ảnh nền
                background.paste(foreground, position, foreground)
            # ----------------------------------------------------------
            # dán cuối
            foreground = foreground3.resize(new_size)
            r, g, b, a = foreground.split()
            foreground = Image.merge("RGBA", (b, g, r, a))

            # Dán ảnh dán vào vị trí position trên ảnh nền
            position = (x + len_mess, y)
            background.paste(foreground, position, foreground)
            
        if line == 2:
            new_size = (1000, 350)
            # dán đầu
            foreground = foreground1.resize(new_size)
            r, g, b, a = foreground.split()
            foreground = Image.merge("RGBA", (b, g, r, a))

            # Dán ảnh dán vào vị trí position trên ảnh nền
            if type == 0:
                position = (x - 150, y + 40)
            else:
                position = (x - 200, y + 40)
            background.paste(foreground, position, foreground)
            # ----------------------------------------------------------
            new_size_ = (len_mess - 300, 500)
            # width, height = foreground2.size
            # print(width, height, len_mess)
            position = (x + 300, y-msg_line_spacing + 69)
            foreground = foreground2.resize(new_size_)
            r, g, b, a = foreground.split()
            foreground = Image.merge("RGBA", (b, g, r, a))
            background.paste(foreground, position, foreground)
            # ----------------------------------------------------------
            # dán cuối
            foreground = foreground3.resize(new_size)
            r, g, b, a = foreground.split()
            foreground = Image.merge("RGBA", (b, g, r, a))

            # Dán ảnh dán vào vị trí position trên ảnh nền
            if type == 1:
                position = (x + len_mess - 500, y + 40)
            else:
                position = (x + len_mess - 400, y + 40)
            background.paste(foreground, position, foreground)

        if line == 3:
            new_size = (1000, 550)
            # dán đầu
            foreground = foreground1.resize(new_size)
            r, g, b, a = foreground.split()
            foreground = Image.merge("RGBA", (b, g, r, a))

            # Dán ảnh dán vào vị trí position trên ảnh nền
            if type == 1:
                position = (x , y -20)
            else:
                position = (x - 100, y - 20)
            background.paste(foreground, position, foreground)
            # ----------------------------------------------------------
            # dán giữa
            new_size_ = (len_mess-100, 737)
            position = (x + 200, y-msg_line_spacing - 15)
            foreground = foreground2.resize(new_size_)
            r, g, b, a = foreground.split()
            foreground = Image.merge("RGBA", (b, g, r, a))
            background.paste(foreground, position, foreground)
            # ----------------------------------------------------------
            # dán cuối
            foreground = foreground3.resize(new_size)
            r, g, b, a = foreground.split()
            foreground = Image.merge("RGBA", (b, g, r, a))

            # Dán ảnh dán vào vị trí position trên ảnh nền
            if type == 1:
                position = (x + len_mess - 600, y - 20)
            else:
                position = (x + len_mess - 700, y - 20)
            background.paste(foreground, position, foreground)
            
        if line == 4:
            new_size = (1000, 560)
            # dán đầu
            foreground = foreground1.resize(new_size)
            r, g, b, a = foreground.split()
            foreground = Image.merge("RGBA", (b, g, r, a))

            # Dán ảnh dán vào vị trí position trên ảnh nền
            position = (x, y - 10)
            background.paste(foreground, position, foreground)
            # ----------------------------------------------------------
            # dán giữa
            new_size_ = (len_mess-100, 922)
            position = (x + 200, y-msg_line_spacing - 45)
            foreground = foreground2.resize(new_size_)
            r, g, b, a = foreground.split()
            foreground = Image.merge("RGBA", (b, g, r, a))
            background.paste(foreground, position, foreground)
            # ----------------------------------------------------------
            # dán cuối
            foreground = foreground3.resize(new_size)
            r, g, b, a = foreground.split()
            foreground = Image.merge("RGBA", (b, g, r, a))

            # Dán ảnh dán vào vị trí position trên ảnh nền
            if type == 1:
                position = (x + len_mess - 600, y - 10)
            else:
                position = (x + len_mess - 700, y - 10)
            background.paste(foreground, position, foreground)

        if line == 5:
            new_size = (1000, 600)
            # dán đầu
            foreground = foreground1.resize(new_size)
            r, g, b, a = foreground.split()
            foreground = Image.merge("RGBA", (b, g, r, a))

            # Dán ảnh dán vào vị trí position trên ảnh nền
            if type == 1:
                position = (x + 100, y + 40)
            else:
                position = (x - 30, y + 40)
            background.paste(foreground, position, foreground)
            # ----------------------------------------------------------
            # # dán giữa
            # new_size_ = (len_mess-100, 1220)
            # position = (x + 200, y-msg_line_spacing - 124)
            # foreground = foreground2.resize(new_size_)
            # r, g, b, a = foreground.split()
            # foreground = Image.merge("RGBA", (b, g, r, a))
            # background.paste(foreground, position, foreground)
            # ----------------------------------------------------------
            # dán cuối
            foreground = foreground3.resize(new_size)
            r, g, b, a = foreground.split()
            foreground = Image.merge("RGBA", (b, g, r, a))

            # Dán ảnh dán vào vị trí position trên ảnh nền
            if type == 1:
                position = (x + len_mess - 650, y + 40)
            else:
                position = (x + len_mess - 750, y + 40)
            background.paste(foreground, position, foreground)

        background = np.array(background)
        return background


    # read file
    with open("input\input.txt", "r", encoding='utf-8') as f:
        message = f.read()

    conversations = []
    for i, line in enumerate(message.splitlines()):
        # 2 kí tự đầu là số thứ tự người chat
        name = line[:2]
        # Nội dung chat là các kí tự còn lại
        message = line[3:]
        # Thêm thông tin người chat vào danh sách
        if name != '1.' and name != '2.':
            name = 0
            # bỏ các kí tự không phải là chữ cái
            message = re.sub(r'[^a-zA-Z0-9 ]', '', message)
        conversations.append({"name": name, "message": message})

    # Khởi tạo đối tượng VideoWriter để ghi video
    video = cv2.VideoWriter('chat.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width_frame, height_frame))

    print('START MAKING VIDEO.....')

    # tittle 
    tittle = cv2.imread('asset/Background.png')
    tittle = cv2.resize(tittle, (width_frame, height_frame))
    # cut bỏ nền trắng
    tittle = tittle[0:110, 0:width_frame]

    # # set avatar
    avatar = cv2.imread('asset/avt1.png')
    avatar = cv2.resize(avatar, (150, 150))
    # add background to frame
    frame = background

    # lấy unique name
    people = []
    for conversation in conversations:
        people.append(conversation['name'])

    # chèn chữ vào tittle
    img_pil = Image.fromarray(tittle)
    draw = ImageDraw.Draw(img_pil)
    draw.text((200, 10),  'Linda', font = font, fill = (255, 255, 255))
    tittle = np.array(img_pil)

    # add tittle to frame
    frame = insert_image(background, tittle, 0, 0)

    # link file audio
    path_audi = "input/voice/"
    files_audi = os.listdir(path_audi)
    sorted_files_audi = sorted(files_audi, key=lambda x: int(x.split('.')[0]))
    audi_index = -1

    x = msg_start_x
    y = msg_start_y

    # giới hạn độ dài tin nhắn thì xuống dòng mới
    max_len_message = 30

    # Duyệt qua từng đoạn hội thoại
    for i, conversation in enumerate(conversations):
        
        # Lấy tên người gửi và nội dung tin nhắn
        name = conversation["name"]
        message = conversation["message"]

        if name == 0:
            # tạo frame mới
            frame = insert_image(background, tittle, 0, 0)
            video.write(frame)
            x = width_frame//2 - 200
            y = height_frame//2
            # viết từng kí tự trong text vào frame
            for j in range(len(message)):
                img_pil = Image.fromarray(frame)
                draw = ImageDraw.Draw(img_pil)
                draw.text((x,y),  message[j], font = font, fill = (255, 255, 255), size = 100)
                frame = np.array(img_pil)
                x += font.getsize(message[j])[0]
                video.write(frame)

            # đọc 4s frame trắng
            for j in range(4):
                video.write(frame)
            frame = insert_image(background, tittle, 0, 0)
            x = msg_start_x
            y = msg_start_y
            continue

        # Nếu tin nhắn hiện tại không còn nằm trong khung hình thì tạo khung hình mới
        if y + msg_spacing > height_frame//5*4:
            frame = insert_image(background, tittle, 0, 0)
            x = msg_start_x
            y = msg_start_y

        # kiểm tra độ dài tin nhắn và tin nhắn đã hết câu
        message_remain = message
        # tính độ dài tin nhắn
        width_message = font.getsize(message)[0]

        if name == '1.':
            # draw avatar
            # Tạo đối tượng hình ảnh PIL từ mảng numpy của ảnh
            avatar_ = Image.fromarray(avatar)
            frame_ = Image.fromarray(frame)
            frame = avt_draw(frame_, avatar_, x-300, y-100)
            max_width_chat = 0
            chat_split = []
            kt = 0
            while len(message_remain) > max_len_message + 10:
                kt = 1
            # tìm vị trí khoảng trắng cuối cùng
                space = message_remain.rfind(' ', 0, max_len_message + 10)
                # tách tin nhắn
                message = message_remain[:space]
                message_remain = message_remain[space+1:]
                chat_split.append(message)
                width_message = font.getsize(message)[0]
                if width_message > max_width_chat:
                    max_width_chat = width_message
            
            while font.getsize(message_remain)[0] < 200 and kt == 0:
                message_remain = ' ' + message_remain + ' '
            # find max len chat
            chat_split.append(message_remain)
            if font.getsize(message_remain)[0] > max_width_chat:
                max_width_chat = font.getsize(message_remain)[0]
            
            # tạo khung tin nhắn
            frame = frame_chat(frame, x-150, y-100, max_width_chat, len(chat_split))
            # Hiển thị nội dung tin nhắn
            img_pil = Image.fromarray(frame)
            draw = ImageDraw.Draw(img_pil)
            for i, chat in enumerate(chat_split):
                draw.text((x, y),  chat, font = font, fill = (0, 0, 0))
                y = y + msg_line_spacing
            y = y + msg_line_spacing
            frame = np.array(img_pil)
        else:
            max_width_chat = 0
            chat_split = []
            while len(message_remain) > max_len_message + 10:
            # tìm vị trí khoảng trắng cuối cùng
                space = message_remain.rfind(' ', 0, max_len_message + 10)
                # tách tin nhắn
                message = message_remain[:space]
                message_remain = message_remain[space+1:]
                chat_split.append(message)
                width_message = font.getsize(message)[0]
                if width_message > max_width_chat:
                    max_width_chat = width_message
            while font.getsize(message_remain)[0] < 200:
                message_remain = ' ' + message_remain + ' '
            # find max len chat
            chat_split.append(message_remain)
            if font.getsize(message_remain)[0] > max_width_chat:
                max_width_chat = font.getsize(message_remain)[0]
            # tạo khung tin nhắn
            if len(chat_split) == 1:
                frame = frame_chat(frame, width_frame - max_width_chat - x//2-150, y-100, max_width_chat, len(chat_split), 1)
            else:
                frame = frame_chat(frame, width_frame - max_width_chat - x//2-200, y-100, max_width_chat, len(chat_split), 1)
            # Hiển thị nội dung tin nhắn
            img_pil = Image.fromarray(frame)
            draw = ImageDraw.Draw(img_pil)
            for i, chat in enumerate(chat_split):
                draw.text((width_frame - max_width_chat - x//2, y),  chat, font = font, fill = (255, 255, 255))
                y = y + msg_line_spacing
            y = y + msg_line_spacing
            frame = np.array(img_pil)

        audi_index += 1
        # thêm audio
        try:
            audio = AudioFileClip(path_audi + sorted_files_audi[audi_index])
            # Lấy thời lượng của file âm thanh
            audio_duration = audio.duration
            # Thêm khung hình hiện tại vào video
            for j in range((round(audio_duration) + 1)):
                video.write(frame)
        except:
            for j in range(4):
                video.write(frame)

    video.release()
    # intro.release()
    # print('----------------------------DONE!-----------------------------')

if __name__ == "__main__":
    main()