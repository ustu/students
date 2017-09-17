${group_name}
${len(group_name) * '='}

.. list-table:: Успеваемость (`${course.name} <http://lectureswww.readthedocs.io/>`_)
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
     %if obj.github:
     - `${obj.github} <https://github.com/${obj.github}>`_
     %else:
     -
     %endif
     %for _checkpoint in obj.checkpoints(course):
     - \
       %for key, value in _checkpoint.items():
         %if isinstance(value, collections.MutableSequence) :
           %for _item in value:
             `${key}.${loop.index+1} <${_item}>`__ \
           %endfor
         %else:
           `${key} <${value}>`__ \
         %endif
         %if loop.last:
           ${""}
         %endif
       %endfor
     %endfor

     %endfor
