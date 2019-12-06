#!/usr/bin/env python3
#-*- coding:utf-8 -*-

class ChineseAreas(object):
    """
    An class for POI areas separated.
    """
    def __init__(self):
        self._areas = {}
        self._areas['dongbei'] = ['辽宁省', '吉林省', '黑龙江省']
        self._areas['huabei'] = ['北京市', '天津市', '河北省', '内蒙古自治区', '山西省']
        self._areas['huazhong'] = ['河南省', '湖北省', '湖南省']
        self._areas['huadong_north'] = ['山东省', '安徽省', '江西省']
        self._areas['huadong_south'] = ['上海市', '江苏省', '浙江省', '福建省', '台湾省']
        self._areas['huanan'] = ['广东省', '广西壮族自治区', '海南省', '香港特别行政区', '澳门特别行政区']
        self._areas['xibei'] = ['陕西省', '甘肃省', '宁夏回族自治区', '青海省', '新疆维吾尔自治区']
        self._areas['xinan'] = ['重庆市', '四川省', '贵州省', '云南省', '西藏自治区']
        self._areas[None] = None

        self._areasName = {}
        self._areasName['dongbei'] = '东北'
        self._areasName['huabei'] = '华北'
        self._areasName['huazhong'] = '华中'
        self._areasName['huadong_north'] = '华东北部'
        self._areasName['huadong_south'] = '华东南部'
        self._areasName['huanan'] = '华南'
        self._areasName['xibei'] = '西北'
        self._areasName['xinan'] = '西南'
        self._areasName[None] = None


    def GetAreasCode(self):
        """
        return all areas key.
        """
        return [key for key in self._areas]

    def GetAreas(self):
        """
        return all areas' Chinese names.
        """
        return [self._areasName[key] for key in self._areas]

    def GetProvince(self):
        """
        return all province names.
        """
        return [self._areas[key] for key in self._areas]

    def GetAreaProvince(self, area):
        """
        return province names in specified area.
        """
        return self._areas[area]

    def GetAreaCode(self, province):
        """
        return area key for specified province.
        """
        for key in self._areas:
            if province in self._areas[key]:
                return key
        return None

    def GetArea(self, province):
        """
        return area Chinese name for specified proince.
        """
        return self._areasName[self.GetAreaCode(province)]

    def __str__(self):
        tmpStr = ''
        for key in self._areas:
            tmpStr += '{} -> {} -> {}\n'.format(key, self._areasName[key], self._areas[key])
        return tmpStr