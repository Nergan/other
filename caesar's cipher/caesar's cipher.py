[
	[
		[
			print
			(
				'''
					____________________________________________________\n
        				\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t
				'''
        		,                                
        		end                            # 足   # 渡   # 春
        		=                              # 弱   # り   # の
        		''                             # の   # て   # 水
			)                 	              # 濁
		]                                             # る
		,
		[
			print
            		(
				alp
                		[
					(
						alp.index
                        			(
							ch
						)
        					+
        					key
					)
    					%
        				54
				]
				,
				end       
				=                             
				''                            
			)                                   
 
			if
			ch
			in
			alp
    			else
 
			print
            		(
				ch
				,
				end
				=
				''
			)
 
			for
			ch
			in
			txt
		]
	]
 
	for
		txt
		,
		key
		,
		alp
	in
 
    zip
    (
        [
            input
            (
                '''
                    txt: 
                '''
            )
        ]
        ,
        [
            int
            (
                input
                (
                    '''
                        key: 
                    '''
                )
            )
        ]
        ,
        [
            'ABCDEFGHIJKLMNOPQPRSTUVWXYZabcdefghijklmnopqprstuvwxyz'
        ]
    )
]