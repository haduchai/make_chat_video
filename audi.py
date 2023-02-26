from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import os
import glob

def main():
    print('Start audio ....')
    path = "input/voice/"
    files = os.listdir(path)
    sorted_files = sorted(files, key=lambda x: int(x.split('.')[0]))

    # Đọc file video
    video = VideoFileClip("chat.mp4")

    # Đọc file âm thanh
    audio = AudioFileClip(path + sorted_files[0])

    # Lấy thời lượng của file âm thanh
    audio_duration = audio.duration

    # Tạo một phần video từ video ban đầu từ thời điểm bắt đầu tới thời điểm kết thúc cần chèn âm thanh
    video_part = video.subclip(0, audio_duration)
    start_audi = audio_duration

    # Thêm âm thanh vào phần video vừa tạo
    video_part_with_audio = video_part.set_audio(audio)

    # # Kết hợp các phần video lại với nhau
    video_part_pre = video_part_with_audio

    for i in range(1, len(sorted_files)):
        # Đọc file âm thanh
        audio = AudioFileClip(path + sorted_files[i])

        # Lấy thời lượng của file âm thanh
        audio_duration = round(audio.duration) + 1

        # Tạo một phần video từ video ban đầu từ thời điểm bắt đầu tới thời điểm kết thúc cần chèn âm thanh
        video_part = video.subclip(start_audi + 1, start_audi + audio_duration)
        start_audi += audio_duration

        # Thêm âm thanh vào phần video vừa tạo
        video_part_with_audio = video_part.set_audio(audio)

        # # Kết hợp các phần video lại với nhau
        video_part_pre = concatenate_videoclips([video_part_pre, video_part_with_audio])

    # Lưu video
    video_part_pre.write_videofile("output.mp4")

if __name__ == '__main__':
    main()