${group_name}
${len(group_name) * '='}

.. list-table:: Успеваемость (${course.name})
   :header-rows: 1
   :stub-columns: 1

   * -
     - ФИО
     - github
     % for i in course.checkpoints:
     - ${i}
     %endfor

     % for obj in students:

   * - ${loop.index+1}
     - ${obj.name}
     - `${obj.github} <https://github.com/${obj.github}>`_
     %for _checkpoint in obj.checkpoints(course):
     - \
       %for key, value in _checkpoint.items():
         %if loop.last:
           `${key} <${value}>`__
         %else:
           `${key} <${value}>`__ \
         %endif
       %endfor
     %endfor

     %endfor
