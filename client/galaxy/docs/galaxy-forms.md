## Forms

Manually crafted "tool" form class, this is broken in the BS4 branch I think.

```vue
<div class="tool-form">
  <form name="foo">
     <div class="form-row">
       <label>Label Input 1</label>
       <input id="input1" type="text" name="input1" size="40" />
     </div>
     <div class="form-row">
       <input type="submit" id="send" name="submit" value="submit" />
     </div>
  </form>
</div>
```

Portlet variant generated by mvc.form.form-view

```vue
<div class="ui-portlet-limited" id="uid-8">
  <div class="portlet-header">
  <div class="portlet-operations"></div>
  <div class="portlet-title">
    <i class="portlet-title-icon fa fa-unlock-alt" style="display: inline;"></i>
    <span class="portlet-title-text">Portlet Title</span></div>
  </div>
  <div class="portlet-content">
    <div class="portlet-body">
	  <div class="ui-message alert alert-info"></div>
	  <div>
	    <div class="ui-form-element section-row">
		  <div class="ui-form-error ui-error"><span class="fa fa-arrow-down"></span><span class="ui-form-error-text"></span></div>
		  <div class="ui-form-title">
		  	<div class="ui-form-collapsible" style="display: none;">
		  	  <i class="ui-form-collapsible-icon"></i>
		  	  <span class="ui-form-collapsible-text"></span>
		  	</div>
		  	<span class="ui-form-title-text">Text Field 1</span>
		  </div>
		  <div class="ui-form-field">
		  	<input class="ui-input" id="field-uid-4" type="text">
		  	<span class="ui-form-info"></span>
		  	<div class="ui-form-backdrop" style="display: none;"></div>
		  </div>
		  <div class="ui-form-preview" style="display: none;"></div>
		</div>
		<div class="ui-form-element section-row">
		  <div class="ui-form-error ui-error" style="display: none;"><span class="fa fa-arrow-down"></span><span class="ui-form-error-text"></span></div>
		  <div class="ui-form-title"><div class="ui-form-collapsible" style="display: none;"><i class="ui-form-collapsible-icon"></i><span class="ui-form-collapsible-text"></span></div><span class="ui-form-title-text" style="display: inline;">Password</span></div>
		  <div class="ui-form-field">
		  	<input class="ui-input" type="password"><span class="ui-form-info"></span><div class="ui-form-backdrop" style="display: none;"></div></div><div class="ui-form-preview" style="display: none;"></div></div>
		<div class="ui-form-element section-row" id="uid-7" style="display: none;"><div class="ui-form-error ui-error" style="display: none;"><span class="fa fa-arrow-down"></span><span class="ui-form-error-text"></span></div><div class="ui-form-title"><div class="ui-form-collapsible" style="display: none;"><i class="ui-form-collapsible-icon"></i><span class="ui-form-collapsible-text"></span></div><span class="ui-form-title-text" style="display: inline;">token</span></div><div class="ui-form-field"><div id="field-uid-7"><div style="display: none;"></div><div></div></div><span class="ui-form-info"></span><div class="ui-form-backdrop" style="display: none;"></div></div><div class="ui-form-preview" style="display: none;"></div></div></div></div><div class="portlet-buttons"><button type="button" class="ui-button-default btn btn-primary ui-clear-float" id="submit" data-original-title="" title=""><i class="icon fa fa-save ui-margin-right"></i><span class="title">Submit</span><div class="progress" style="display: none;"><div class="progress-bar" style="width: 0%;"></div></div></button></div></div><div class="portlet-backdrop"></div></div>
```