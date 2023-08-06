from typing import List, Dict
from PIL import Image, ExifTags, TiffImagePlugin

import json
import numbers


class GPSInfoHeader():
    def __init__(self, **fields):
        self._fields = fields

    def __iter__(self):
        for key in self._fields:
            yield (key, self._fields[key],)

    @classmethod
    def get_map_link(self, N=0, W=0):
        ndeg = str(round(float(N[0]),2))
        nhour = str(round(float(N[1]),2))
        nsec = f"{round(float(N[2]),2):.2f}"
        wdeg = str(round(float(W[0]),2))
        whour = str(round(float(W[1]),2))
        wsec = f"{round(float(W[2]),2):.2f}"

        # build the link in a way that the string can be read on the command line
        return r"https://www.google.com/maps/place/" + ndeg+r"°"+nhour+r"\'"+nsec+r'\"N+' + wdeg+r'°'+whour+r"\'"+wsec+r'\"W/'

class GPSInfoHeaderEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class ExifHeader():
    def __init__(self, **fields):
        self._fields = fields

    def __iter__(self):
        for key in self._fields:
            yield (key, self._fields[key],)

class ExifHeaderEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__
    

class ExifHeaderListParser():
    def __init__(self, jpgs: List[str]):
        self.items: Dict[str, dict] = dict()
        self.jpgs: List[str] = jpgs
        self.visible_exif_field = {'ApertureValue':True, 'BrightnessValue':True, 'ColorSpace':True, 
                                      'ComponentsConfiguration':True, 'DateTime':True, 'DateTimeDigitized':True, 
                                      'DateTimeOriginal':True, 'DigitalZoomRatio':True, 'ExifImageHeight':True, 
                                      'ExifImageWidth':True, 'ExifInteroperabilityOffset':True, 'ExifOffset':True, 
                                      'ExifVersion':True, 'ExposureBiasValue':True, 'ExposureMode':True, 'ExposureProgram':True, 
                                      'ExposureTime':True, 'FNumber':True, 'Flash':True, 'FlashPixVersion':True, 'FocalLength':True,
                                      'FocalLengthIn35mmFilm':True, 'GPSInfo':True,  'ISOSpeedRatings':True, 'ImageDescription':True,
                                      'ImageLength':True, 'ImageWidth':True, 'LightSource':True, 'Make':True, 'MakerNote':True, 
                                      'MaxApertureValue':True, 'MeteringMode':True, 'Model':True, 'Orientation':True, 
                                      'RecommendedExposureIndex':True, 'ResolutionUnit':True, 'SceneCaptureType':True, 
                                      'SceneType':True, 'SensingMethod':True, 'SensitivityType':True, 'ShutterSpeedValue':True, 
                                      'Software':True, 'SubsecTime':True, 'SubsecTimeDigitized':True, 'SubsecTimeOriginal':True, 
                                      'WhiteBalance':True, 'XResolution':True, 'YCbCrPositioning':True, 'YResolution':True}
        self.visible_gps_field = {'GPSVersionID':True,'GPSLatitudeRef':True,'GPSLatitude':True,'GPSLongitudeRef':True,
                                     'GPSLongitude':True,'GPSAltitudeRef':True,'GPSAltitude':True,'GPSTimeStamp':True,
                                     'GPSSatellites':True,'GPSStatus':True,'GPSMeasureMode':True,'GPSDOP':True,'GPSSpeedRef':True,
                                     'GPSSpeed':True,'GPSTrackRef':True,'GPSTrack':True,'GPSImgDirectionRef':True,'GPSImgDirection':True,
                                     'GPSMapDatum':True,'GPSDestLatitudeRef':True,'GPSDestLatitude':True,'GPSDestLongitudeRef':True,
                                     'GPSDestLongitude':True,'GPSDestBearingRef':True,'GPSDestBearing':True,'GPSDestDistanceRef':True,
                                     'GPSDestDistance':True,'GPSProcessingMethod':True,'GPSAreaInformation':True,'GPSDateStamp':True,
                                     'GPSDifferential':True,'GPSHPositioningError':True}
    
    def __str__(self):
       return json.dumps(self.items, cls=ExifHeaderEncoder)


    def parse(self):
        
        if len(self.jpgs) == 0:
            raise Exception('No files to process')
        
        for i in range(len(self.jpgs)):
            exif_dict = None
        
            with Image.open(self.jpgs[i]) as img:
                exif_dict = img._getexif()

            image_name = str(self.jpgs[i])

            if exif_dict is None:
                raise Exception(f"No exif data for image {image_name}")

            exif_data = {
                ExifTags.TAGS[k]: v for k, v in exif_dict.items() if k in ExifTags.TAGS
            }

            exif_header = {
                k: None for k, _ in exif_data.items()
            }

            keys = dict(exif_header).keys()
            for k, v in exif_data.items():
                if not self.visible_exif_field[k]:
                    if k in keys:
                        del exif_header[k]
                        continue
                if not isinstance(v, numbers.Integral) and isinstance(v, numbers.Rational):
                    exif_header[k] = float(v)
                elif isinstance(v, bytes):
                    exif_header[k] = str(v)
                elif k == 'GPSInfo':
                    gps_info = {ExifTags.GPSTAGS[gk]:gv for gk, gv in exif_data[k].items() if gk in ExifTags.GPSTAGS}
                    gps_info_header = {gps_info_key: None for gps_info_key, _ in gps_info.items()}
                    gps_info_header_keys = dict(gps_info_header).keys()
                    for gk, gv in gps_info.items():
                        if not self.visible_gps_field[gk]:
                            if gk in gps_info_header_keys:
                                del gps_info_header[gk]
                                continue
                        if not isinstance(gps_info[gk], numbers.Integral) and isinstance(gps_info[gk], numbers.Rational):
                            gps_info_header[gk] = float(gps_info[gk])
                        elif isinstance(gps_info[gk], bytes):
                            gps_info_header[gk] = str(gps_info[gk])
                        elif isinstance(gps_info[gk], tuple):
                            gps_info_header[gk] = tuple([float(r) for r in gps_info[gk] if \
                                                        not isinstance(r, numbers.Integral) \
                                                        and isinstance(r, TiffImagePlugin.IFDRational)])
                        else:
                            gps_info_header[gk] = gps_info[gk]

                    gps_info_header['MapLink'] = GPSInfoHeader.get_map_link(
                        N=gps_info_header['GPSLatitude'],
                        W=gps_info_header['GPSLongitude'],
                    )                   
            fields = {
                **{k:f for k, f in exif_header.items()},
                'GPSInfo': GPSInfoHeader(**gps_info_header)._fields
            }               

            self.items[image_name] = ExifHeader(**fields)._fields

