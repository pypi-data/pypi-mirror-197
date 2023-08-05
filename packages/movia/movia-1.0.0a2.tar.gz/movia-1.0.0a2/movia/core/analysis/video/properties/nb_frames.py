#!/usr/bin/env python3

"""
** Recover the number of frames in a video stream. **
-----------------------------------------------------

This allows not only the characteristics of the files but also the tags if there are any.
"""

import collections
import pathlib
import typing

import cv2 # pip install opencv-contrib-python-headless

from movia.core.exceptions import MissingStreamError, MissingInformation
from movia.core.analysis.video.properties.parser import (_check_pathexists_index,
    _decode_duration_frames_ffmpeg, _mix_and_check, _parse_ffprobe_res)


def _count_frames_ffmpeg(filename: str, index: int) -> int:
    """
    ** Count the number of frames with the ffmpeg decoder. **

    Slow but 100% accurate method.

    Examples
    --------
    >>> from movia.core.analysis.video.properties.nb_frames import _count_frames_ffmpeg
    >>> _count_frames_ffmpeg("movia/examples/video.mp4", 0)
    400
    >>>
    """
    _, frames = _decode_duration_frames_ffmpeg(filename, index)
    return frames

def _count_frames_cv2(filename: str, index: int) -> int:
    """
    ** Count the number of frames with the cv2 decoder. **

    Slow but 100% accurate method.

    Examples
    --------
    >>> from movia.core.analysis.video.properties.nb_frames import _count_frames_cv2
    >>> _count_frames_cv2("movia/examples/video.mp4", 0)
    400
    >>>
    """
    cap = cv2.VideoCapture(filename, index)
    if not cap.isOpened():
        raise MissingStreamError(f"impossible to open '{filename}' stream {index} with 'cv2'")
    frames = 0
    while True:
        if not cap.read()[0]:
            break
        frames += 1
    cap.release()
    if not frames:
        raise MissingStreamError(f"'cv2' did not find any frames '{filename}' stream {index}")
    return frames

def _estimate_frames_ffmpeg(filename: str, index: int) -> int:
    """
    ** Extract the number of frames from the metadata. **

    Very fast method but inaccurate. It doesn't work all the time.

    Examples
    --------
    >>> from movia.core.analysis.video.properties.nb_frames import _estimate_frames_ffmpeg
    >>> _estimate_frames_ffmpeg("movia/examples/video.mp4", 0)
    400
    >>>
    """
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", f"v:{index}", "-show_entries", "stream=nb_frames",
        "-of", "default=nokey=1:noprint_wrappers=1",
        filename,
    ]
    frames = _parse_ffprobe_res(cmd, filename, index)
    return int(frames)

def _estimate_frames_cv2(filename: str, index: int) -> int:
    """
    ** Extract the number of frames from the metadata. **

    Very fast method but inaccurate. It doesn't work all the time.

    Examples
    --------
    >>> from movia.core.analysis.video.properties.nb_frames import _estimate_frames_cv2
    >>> _estimate_frames_cv2("movia/examples/video.mp4", 0)
    400
    >>>
    """
    cap = cv2.VideoCapture(filename, index)
    if not cap.isOpened():
        raise MissingStreamError(f"impossible to open '{filename}' stream {index} with 'cv2'")
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    if frames <= 0: # we saw a case at -553402322211286528
        raise MissingInformation(f"'cv2' does not detect any frame in '{filename}' stream {index}")
    return frames

def get_nb_frames(
    filename: typing.Union[str, bytes, pathlib.Path],
    index: int=0,
    *,
    backend: typing.Union[None, str]=None,
    accurate: bool=False,
) -> int:
    """
    ** Recovers the number of frames present in a video stream. **

    Parameters
    ----------
    filename : pathlike
        The pathlike of the file containing a video stream.
    index : int
        The index of the video stream being considered,
        by default the first stream encountered is selected.
    backend : str, optional
        - None (default) : Try to read the stream by trying differents backends.
        - 'ffmpeg' : Uses the modules ``pip3 install ffmpeg-python``
            which are using the ``ffmpeg`` program in the background.
        - 'cv2' : Uses the module ``pip3 install opencv-contrib-python-headless``.
    accurate : boolean, optional
        If True, recovers the number of frames by fully decoding all the frames in the video.
        It is very accurate but very slow. If False (default),
        first tries to get the frame count from the file metadata.
        It's not accurate but very fast.

    Returns
    -------
    nbr : int
        The number of readed frames.

    Raises
    ------
    MissingStreamError
        If the file does not contain a playable video stream.
    MissingInformation
        If the information is unavailable.
    """
    _check_pathexists_index(filename, index)

    return _mix_and_check(
        backend, accurate, (str(pathlib.Path(filename)), index),
        collections.OrderedDict([
            (_estimate_frames_ffmpeg, {"accurate": False, "backend": "ffmpeg"}),
            (_estimate_frames_cv2, {"accurate": False, "backend": "cv2"}),
            (_count_frames_ffmpeg, {"accurate": True, "backend": "ffmpeg"}),
            (_count_frames_cv2, {"accurate": True, "backend": "cv2"}),
        ])
    )
