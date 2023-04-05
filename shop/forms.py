from django import forms

class OrderStatusChangeListForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrderStatusChangeListForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            # self.fields['book'].queryset = Book.objects.filter(
            #     size=instance.size
            # )
            if instance.complete ==  False:
                # print(LabeledHiddenInput())
                self.fields['status'].widget = LabeledHiddenInput()

class LabeledHiddenInput(forms.widgets.HiddenInput):
    def render(self, name, value, attrs=None, renderer=None):
        base_output = super(LabeledHiddenInput, self).render(name, value, attrs)
        if value:
            print("base_output", base_output + str(value))
            return base_output + str(value)
        else:
        	# print(value)
            return base_output