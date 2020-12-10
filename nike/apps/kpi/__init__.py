# -*- coding:utf8  -*-
from apps.kpi.views import *
from apps.kpi.models import *

def regist_kpi(api):
    # 一些KPI图表
    api.add_resource(CenterUpDatabase, '/Center_UpDatabase')
    api.add_resource(TransportUpDatabase, '/Transport_UpDatabase')
    api.add_resource(KPIVisualize, '/KPI_Visualize')
    api.add_resource(RANKVisualize, '/Rank_Visualize')
    api.add_resource(KPIScore, '/Nike_KPI_Score')
    api.add_resource(TransportShowKPI, '/Transport_ShowKPI')