
__all__ = ('conection_str',)

__username = 'sys'
__password = 'dreyevihor'
__host = 'localhost'
__port = 1521
__tnsname = 'xe'

conection_str = __username+'/'+__password+'@'+__host+':'+str(__port)+'/'+__tnsname