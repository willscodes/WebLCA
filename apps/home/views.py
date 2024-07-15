# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
import olca_ipc as ipc
import olca_schema as o

def lca_api_call(request):
    # 创建IPC客户端
    client = ipc.Client(8080)

    try:
        # 获取Process的描述符
        descriptors = client.get_descriptors(o.Process)
        results = []

        for descriptor in descriptors[:20]:  # 只获取前20个描述符
            detailed_info = client.get(o.Process, descriptor.id)
            if detailed_info.process_documentation and detailed_info.process_documentation.data_set_owner:
                data_set_owner = detailed_info.process_documentation.data_set_owner
                result = {
                    'id': descriptor.id,
                    'type': 'Process',
                    'name': data_set_owner.name  # Directly include the name here
                }
                results.append(result)

        return JsonResponse({'success': True, 'results': results})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    try:
        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def lca_api_test(request):
    context = {'segment': 'lca_api_test'}
    html_template = loader.get_template('home/lca_api_test.html')
    return HttpResponse(html_template.render(context, request))


