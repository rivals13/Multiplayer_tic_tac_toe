rule Detect_Image_Malware {
    strings:
        // this will detect the  common malicious scripts hidden inside image text metadata
        $php_start = "<?php"
        $eval = "eval("
        $system = "system("
        $shell = "/bin/bash"
    condition:
        any of them
    }
