def getAttribute(givenClass):
    attribute = []
    parameter = []
    for i_attribute in dir(givenClass):
        if i_attribute[0] != "_":
            if not hasattr(getattr(givenClass, i_attribute), "__dict__"):
                if getattr(givenClass, i_attribute) is not None:
                    attribute.append(i_attribute)
                    parameter.append(getattr(givenClass, i_attribute))
            else:
                subAttribute, subParameter = getAttribute(
                    getattr(givenClass, i_attribute)
                )
                attribute = attribute + subAttribute
                parameter = parameter + subParameter
    return attribute, parameter
