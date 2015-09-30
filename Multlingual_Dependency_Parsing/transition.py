class Transition(object):
    """
    This class defines a set of transitions which are applied to a
    configuration to get the next configuration.
    """
    # Define set of transitions
    LEFT_ARC = 'LEFTARC'
    RIGHT_ARC = 'RIGHTARC'
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'

    def __init__(self):
        raise ValueError('Do not construct this object!')

    @staticmethod
    def left_arc(conf, relation):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
	if not conf.buffer or not conf.stack:
	    return -1
	stack_top = conf.stack[-1]
	for arc in conf.arcs:
	    k,rel,i = arc
	    if i == stack_top:
		return -1
	conf.stack.pop()
	buffer_head = conf.buffer[0]
        conf.arcs.append((buffer_head, relation,stack_top ))
 
	#raise NotImplementedError('Please implement left_arc!')
        #return -1

    @staticmethod
    def right_arc(conf, relation):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
        if not conf.buffer or not conf.stack:
            return -1
        # You get this one for free! Use it as an example.
        idx_wi = conf.stack[-1]
        idx_wj = conf.buffer.pop(0)

        conf.stack.append(idx_wj)
        conf.arcs.append((idx_wi, relation, idx_wj))
    @staticmethod
    def reduce(conf):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
	if not conf.stack:
	    return -1
    	stack_top = conf.stack[-1]
    	for arc in conf.arcs:
	    k,l,i = arc
	    if i == stack_top:
		conf.stack.pop()
		return 0
	return -1
	#raise NotImplementedError('Please implement reduce!')
        #return -1

    @staticmethod
    def shift(conf):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
	if not conf.buffer:
	    return -1
    	buffer_head = conf.buffer.pop(0)
	conf.stack.append(buffer_head)
	return 0
	#raise NotImplementedError('Please implement shift!')
        #return -1
