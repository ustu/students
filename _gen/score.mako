${group_name}
${len(group_name) * '='}

.. list-table:: Успеваемость (`${course.name} <https://lectureswww.readthedocs.io/>`_)
   :header-rows: 1
   :stub-columns: 1

   * -
     - ФИО
     % for _, values in course.checkpoints_group:
     - `${values.get('name', '')} <${values.get("url", "./")}>`_
     %endfor

   * -
     -
     % for _, values in course.checkpoints_group:
       <%
         date = values.get("date")
       %>
       %if date:
     - ${date.split('/')[0]}/${date.split('/')[1]} ${date.split('/')[2]}
       % else:
     -
       %endif
     %endfor

     % for obj in students:

   * - ${loop.index+1}
     - ${obj.name} \
     %if obj.github:
       (`${obj.github} <https://github.com/${obj.github}>`_)
     %else:

     %endif
     %for _checkpoint in obj.checkpoints(course):
     - \
       %for key, value in _checkpoint.items():
         %if key is not 'score':
           %if isinstance(value, collections.MutableSequence) :
             %for _item in value:
               `${key}.${loop.index+1} <${_item}>`__ \
             %endfor
           %else:
             `${key} <${value}>`__ \
           %endif
         %endif
         %if loop.last:
           %if _checkpoint.get('score', ''):
             [**+${_checkpoint.get('score', '')}**]
           %else:
             ${''}
           %endif
         %endif
       %endfor
     %endfor

     %endfor
