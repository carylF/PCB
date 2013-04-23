$(document).ready(function(){
			
			$('#signup input').hover(function()
			{
				
				$(this).popover('toggle')
			});
			
			$("#signup").validate({
				rules:{
					first_name:"required",
					laast_name:"required",
					email_address:{
							required:true,
							email: true
						},
					password:{
						required:true,
						minlength: 6
					},
					cpwd:{
						required:true,
						equalTo: "#pwd"
					},
					user_type:"required"
					
				},
				messages:{
					first_name:"Enter your first name",
					last_name:"Enter your last name",
					email_address:{
						required:"Enter your email address",
						email:"Enter valid email address"
					},
					password:{
						required:"Enter your password",
						minlength:"Password must be minimum 6 characters"
					},
					cpwd:{
						required:"Confirm password",
						equalTo:"Password and Confirm Password must match"
					},
					user_type:"Select Gender"
				},
				errorClass: "help-inline",
				errorElement: "span",
				highlight:function(element, errorClass, validClass) {
					$(element).parents('.control-group').addClass('error');
				},
				unhighlight: function(element, errorClass, validClass) {
					$(element).parents('.control-group').removeClass('error');
					$(element).parents('.control-group').addClass('success');
				}
			});
		});