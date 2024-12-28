#!/usr/bin/env python3
import os
import shutil
import re

COLLECTION_PREFIX = '合集_'
DELETE_FILE_TYPE = ['info', 'png', 'txt', 'jpg', 'xltd', 'torrent', 'DS_Store', 'js', 'nfo']
TO_BE_DELETED_ORG_NAME = ['阳光电影-www.dygod.org', '电影天堂www.dy2018.com', '电影天堂www.dy2018.net',
                          '动漫东东资源团', 'YYeTs人人影视', '阳光电影dygod.org', 'BT世界网.www.btsj5.com', 'MP4电影www.mp4so.com',
                          '阳光电影www.ygdy8.com', '66影视', 'BT世界网', 'MP4电影', '霸王龙压制组T-Rex', '亿万同人亚译联盟韩语组译制',
                          '人人电影网：www.rrdyw.cc', '人人影视制作', '电影天堂.www.dytt89.com', '非凡科技影视小组',
                          '阳光电影www.ygdy8.net', '九洲客', '电影天堂.www.dytt89.com', '非凡科技影视小组', '霸王龙组T_Rex',
                          '电影天堂', '阳光电影', '人人电影网', '人人', 'www.dy2018.com', 'www.dygod.org', 'dygod.org',
                          'www.ygdy8.com', 'www.ygdy8.net', 'www.dytt89.com', 'www.rrdyw.cc', 'www.dy2018.net',
                          'dy.ygdy8.com', '_FFans',
                          'www.dygod.cn', 'www.dygod.net', 'www.66Ys.Co', 'www.btsj5.com', 'www.mp4so.com',
                          '影视', '压制'
                          ]
TO_BE_DELETED_KEYWORD = [
    '国英', '国语', '韩语', '日语', '中字', '中文', '简体', '粤语', '韩版', '泰语', '英字',
    '中英', '双字', '双语', 'zh', '.韩国.', '.动作.', '中简', '内嵌',
    '中俄法', '国粤英3语', '国粤英', '国粤日', '国德', '国韩', '国粤泰', '泰国粤', '国粤', '三语', '国日', '音轨', '特效', '杜比视界', '奥斯卡',
    '_ENG', 'English', 'Cantonese', 'CHINESE', 'Korean', 'Thai', 'KO_CN', '_KO', '_CN', 'USA', 'JPN',
    '内封字幕', '双字幕', '字幕', '外挂', '幕', '内封', '剧情', '导演剪辑版', 'Directors.Cut'
                                                         'CC标准收藏版', 'RSTERED', '10周年纪念版', '70周年纪念版',
    '70th.Anniversary.Edition',
    '1024分辨率', '超清版', '蓝光', '高清', '精校版', '修复', 'BluRay', '1080p', '720p', '768X576', '1024x560', 'x264', 'x265',
    '1440p', '360p', 'VCDRip', '4K',
    '.Lan.', '1080p.x265', 'H265_DDP2.0_GPT', 'H265_DDP2.0_GPT', 'REMUX', '原盘', 'PROPER', 'HDR10', 'HDR', 'HKFACT',
    'DDP5', 'HDSWEB', 'H265',
    'AC3-CMCT', 'DVDRip', 'WEB-DL', 'DVD', 'AC3-iKHC', 'HR-HDTV', 'Atmos_RARBG', 'KisColourKeKeys',
    'Atmos', '60fps', '265-FLUX', '265_FLUX',
    '\(1\)', 'DTS', 'Chosen1', 'AGAiN',
    'MiniFHD-GOD', 'HDTV', '_KLWNH', '260p', 'UHD', '.MA', 'Atmos', '2160p', '2000bit',
    '10bit', '_CNSCG', '_CMCT', 'WEB_DL',
    '_iKHC', 'CHS-ENG', 'MiniF_GOD', 'HEVC', 'DoVi', '_VXT',
    '5Audios', '4Audios', '3Audios', '2Audios', '5Audio', '4Audio', '3Audio', '2Audio', 'MN_FRDS',
    'xiaopie@CHDWEB', 'CHS', 'TSKS', 'HR_TV', 'Mp4er', '_99Mp4', 'DDP2.0-GPTHD', 'TSKS',
    'GREENOTEA', 'BD', 'Mp4Ba', 'AAC', 'AC3', 'H264', 'HD', 'WEB', 'True', 'DD5',
    '#39;s', 'V1', 'V2', ' ', '@@@', '&', '|', '《', '》', '-', '#', ';',
    'Top\d{1,3}', '^\d{4}'
]
ILLEGAL_SIGN_LIST = ['[', '【', '(']
TO_UNDERLINE_LIST = [']', '】', ')', '__', '-', ' - ', '.DV.', '.DC.', '.CC.']
RETAINED_FILE_TYPE = ['ass', 'mkv', 'mp4', 'rmvb', 'SRT']
TO_SINGLE_DOT = [
    '\.\.', '_\.', '\.en\.', '\.Rip\.', '\._X\.', '\.\d\.\d\.', '\.\d\.', '\.\w\.', '\.HQ\.', '\.NF\.',
    '\.265\.','\.202\d\.','\.201\d\.',
]
SINGLE_DOT = '.'
UNDERLINE = '_'
TO_REPLACEMENT = {'([^\._])(\d{4})\.': r'\1.\2.'}


def rename(oldFileName, rootDir, directory=''):
    newFileName = oldFileName
    # 删除组织名
    for orgName in TO_BE_DELETED_ORG_NAME:
        newFileName = re.sub(orgName, '', newFileName, flags=re.I)
        newFileName = processSign(newFileName)
    for keyword in TO_BE_DELETED_KEYWORD:
        newFileName = re.sub(keyword, '', newFileName, flags=re.I)
        newFileName = processSign(newFileName)
    for k, v in TO_REPLACEMENT.items():
        newFileName = re.sub(k, v, newFileName, flags=re.I)
        newFileName = processSign(newFileName)

    if os.path.isdir(oldFileName):
        for retainedFileType in RETAINED_FILE_TYPE:
            if newFileName.endswith(UNDERLINE + retainedFileType) or newFileName.endswith(
                    SINGLE_DOT + retainedFileType):
                newFileName = newFileName[0:len(newFileName) - len(retainedFileType) - 1]

    oldFileFullFilePath = f'{rootDir}/{directory}/{oldFileName}' if directory else f'{rootDir}/{oldFileName}'
    newFileFullFilePath = f'{rootDir}/{directory}/{newFileName}' if directory else f'{rootDir}/{newFileName}'
    # os.rename(old_file_path, new_file_path), 只能对相应的文件进行重命名, 不能重命名文件的上级目录名.
    # os.renames 能重命名上级目录
    if oldFileName != newFileName:
        os.rename(oldFileFullFilePath, newFileFullFilePath)
        print(f'rename {oldFileName} to {newFileName}')


def processSign(filename):
    for sign in ILLEGAL_SIGN_LIST:
        filename = filename.replace(sign, '')
    for sign in TO_SINGLE_DOT:
        filename = re.sub(sign, SINGLE_DOT, filename, flags=re.I)
    for sign in TO_UNDERLINE_LIST:
        filename = filename.replace(sign, UNDERLINE)
    for sign in TO_SINGLE_DOT:
        filename = re.sub(sign, SINGLE_DOT, filename, flags=re.I)
    if filename.startswith(UNDERLINE) or (filename.startswith(SINGLE_DOT) and filename.rindex(SINGLE_DOT) != 0):
        filename = filename[1:len(filename)]
    return filename


def remove(fileName):
    for extension in DELETE_FILE_TYPE:
        if fileName.endswith(SINGLE_DOT + extension):
            os.remove(fileName)
            print(f'delete {fileName}')
            return True
    return False


def run(currentDir):
    os.chdir(currentDir)
    rootDir = os.getcwd()
    print(f'root is {rootDir}')

    for i in range(3):
        for fileUnderRoot in os.listdir(rootDir):
            if os.path.isdir(fileUnderRoot):
                fileList = os.listdir(fileUnderRoot)
                if fileUnderRoot.startswith(COLLECTION_PREFIX):
                    if i == 0:
                        for subFile in fileList:
                            rename(subFile, rootDir, fileUnderRoot)
                else:
                    if len(fileList):
                        for subFile in fileList:
                            if not remove(f'./{fileUnderRoot}/{subFile}'):
                                if os.path.exists(subFile):
                                    os.rename(f'./{fileUnderRoot}/{subFile}', rootDir,
                                              f'./{fileUnderRoot}/@@@{subFile}')
                                    shutil.move(f'./{fileUnderRoot}/@@@{subFile}', rootDir)
                                else:
                                    shutil.move(f'./{fileUnderRoot}/{subFile}', rootDir)

                    else:
                        print(f'moving {fileUnderRoot}')
                        os.removedirs(fileUnderRoot)
                        print(f'finish moving {fileUnderRoot}')
            else:
                remove(fileUnderRoot)
                if os.path.exists(fileUnderRoot):
                    rename(fileUnderRoot, rootDir)


if __name__ == '__main__':
    run(os.getcwd())
