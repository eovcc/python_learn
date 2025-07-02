import requests
import ffmpeg
import os
import tqdm


def convert_m4s_to_mp4(video_path, audio_path, output_path):
    """使用ffmpeg-python转换M4S为MP4"""
    try:
        # 创建视频输入流
        video_input = ffmpeg.input(video_path)

        # 创建音频输入流
        audio_input = ffmpeg.input(audio_path)

        # 合并并输出
        (
            ffmpeg.output(
                video_input,
                audio_input,
                output_path,
                vcodec="copy",  # 复制视频流
                acodec="copy",  # 转码音频为AAC
                movflags="faststart",  # 网络优化
                loglevel="error",  # 仅显示错误
            )
            .overwrite_output()  # 相当于 -y 参数
            .run()
        )
        print("合并成功...")
        return True

    except ffmpeg.Error as e:
        print(f"FFmpeg错误: {e.stderr.decode('utf8', errors='ignore')}")
        return False
    except Exception as e:
        print(f"未知错误: {str(e)}")
        return False


def main():
    # b站视频和音频分离，需要手动合并
    video_url = """https://xy223x84x46x150xy.mcdn.bilivideo.cn:8082/v1/resource/30690837709-1-30102.m4s?
    agrr=1&build=0&buvid=F22DC8F6-F9B1-97AA-3C67-F86969CB578150668infoc&bvc=vod&bw=571064&deadline=17511
    02192&dl=0&e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03e
    N0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B59
    9M%3D&f=u_0_0&gen=playurlv3&mcdnid=50030489&mid=341674779&nbs=1&nettype=0&og=hw&oi=2742916404&orderid
    =0%2C3&os=mcdn&platform=pc&sign=b394d5&traceid=trpbXgkAeiZetC_0_e_N&uipk=5&uparams=e%2Cgen%2Cog%2Cmid
    %2Cdeadline%2Cuipk%2Cplatform%2Ctrid%2Cnbs%2Coi%2Cos&upsig=5b58d0086097e243be913952dda13376"""
    audio_url = """https://xy36x141x100x19xy.mcdn.bilivideo.cn:8082/v1/resource/30690837709-1-30232.m4s?
    agrr=1&build=0&buvid=F22DC8F6-F9B1-97AA-3C67-F86969CB578150668infoc&bvc=vod&bw=96060&deadline=175110
    2192&dl=0&e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03e
    N0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B5
    99M%3D&f=u_0_0&gen=playurlv3&mcdnid=50030489&mid=341674779&nbs=1&nettype=0&og=cos&oi=2742916404&ord
    erid=0%2C3&os=mcdn&platform=pc&sign=ea3cdf&traceid=trIzFsUVtHdtDi_0_e_N&uipk=5&uparams=e%2Cuipk%2Cos
    %2Cplatform%2Ctrid%2Cmid%2Cdeadline%2Cnbs%2Cgen%2Cog%2Coi&upsig=736f39b787f42771e7c9e319b2009ebf"""
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0"
    }
    v_response = requests.get(url=video_url, stream=True, headers=headers)
    a_response = requests.get(url=audio_url, stream=True, headers=headers)
    print(f"{v_response.status_code=}, {a_response.status_code=}")
    v_filesize = int(v_response.headers.get("Content-Length"))
    a_filesize = int(a_response.headers.get("Content-Length"))
    with open("video.m4s", "wb") as f:
        for chunk in tqdm.tqdm(
            v_response.iter_content(1024),
            desc="video.m4s",
            total=int(v_filesize / 1024) + 1,
            ncols=100,
            unit="kb",
        ):
            f.write(chunk)
    print("视频下载完毕...")
    with open("audio.m4s", "wb") as f:
        for chunk in tqdm.tqdm(
            a_response.iter_content(1024),
            desc="video.m4s",
            total=int(a_filesize / 1024) + 1,
            unit="kb",
            ncols=100,
        ):
            f.write(chunk)
    print("音频下载完毕...")

    convert_m4s_to_mp4("video.m4s", "audio.m4s", "output.mp4")
    os.remove("video.m4s")
    os.remove("audio.m4s")


if __name__ == "__main__":
    main()
