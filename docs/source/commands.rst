****************
Useful Commands
****************

Here is a list of useful commands that you may run into over and over. 

.. list-table:: 
   :widths: 20 50
   :header-rows: 1

   * - Commands
     - Explanation
   * - ``rm`` <item>
     - Remove <item> (add ``-r`` for directories)
   * - ``cp`` <item> <destination>
     - Copy item from <path> to <destination> (add ``-r`` for directories)
   * - ``mv`` <item> <destination>
     - Move item to <destination>
   * - ``ls`` <path>
     - List items in the directory at <path>. If you don't specify <path>, the directory is taken to be the current one (add -ltr for list all files in reverse time order)
   * - ``cd`` <path>
     - Change directory to the given <path> (``cd ..`` to go up one level)
   * - ``mkdir`` <name>
     - Creates a new directory called <name>



****************************
Occasionally Useful Commands
****************************

.. list-table:: 
   :widths: 20 50
   :header-rows: 1

   * - Commands
     - Explanation
   * - ``pwd``
     - Tells you your current path
   * - ``grep -rin`` <item> <destination>
     - Searches for <item> in <destination>, recursively (``-r``), in a case insensitive manner (``-i``), and returns line number (``-n``). 
   * - ``scp -r`` <item> <destination>
     - Uploading <item> to <destination>. ``-r`` for directories. 
   * - ``rsync -avz`` <optional> <item> <destination>
     - Uploading <item> to <destination>, but faster than ``scp``. In <optional>, you can add ``--exclude={"LOGS*",'png','photos'}`` to exlucde things like LOGS folder, png folder, and photos folder, for example. The asterisk ``*`` is a wildcard character. 


****************************
Text Editors
****************************

.. list-table:: 
   :widths: 20 50
   :header-rows: 1

   * - Editors
     - Notes
   * - ``emacs`` (may require installation)
     - ``ctrl+x ctrl+s`` for saving, ``ctrl+x ctrl+c`` for quitting


**************************************
Useful Commands that need installation
**************************************