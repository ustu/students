${group_name}
${len(group_name) * '='}

.. list-table:: Успеваемость
   :header-rows: 1
   :stub-columns: 1

   * -
     - ФИО
     - github
     % for i in checkpoints:
     - ${i}
     %endfor

   * -
     - ФИО
     - github
     % for i in checkpoints:
     - ${i}
     %endfor
