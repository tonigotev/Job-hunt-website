import { useRegister } from "../services/authService";
import { Link, useNavigate } from "react-router-dom";
import { ErrorMessage, Field, Form, Formik } from "formik";
import { registerValidationSchema } from "../utils/validationSchemas";
import InputField from "../components/InputField";
import SubmitButton from "../components/SubmitButton";
import { useState } from "react";

const initialValues = {
   first_name: "",
   last_name: "",
   username: "",
   email: "",
   password: "",
   role: "job_seeker",
};

const Register = () => {
   const { mutateAsync: register } = useRegister();
   const navigate = useNavigate();
   const [apiErrors, setApiErrors] = useState({});

   const handleSubmit = async (
      values,
      { setSubmitting, setFieldError }
   ) => {
      setApiErrors({});
      try {
         const { status, data } = await register({
            first_name: values.first_name,
            last_name: values.last_name,
            username: values.username,
            email: values.email,
            password: values.password,
            role: values.role,
         });

         if (status === "success") {
            navigate("/login", { state: { username: values.username } });
         } else if (status === "error") {
            if (typeof data === "object") {
               // Handle field-specific errors
               Object.keys(data).forEach((field) => {
                  const errorMessage = Array.isArray(data[field]) 
                     ? data[field][0] 
                     : data[field];
                  setFieldError(field, errorMessage);
               });
               // Set general errors
               setApiErrors(data);
            } else {
               setApiErrors({ general: data });
            }
         }
      } catch (error) {
         console.error("Registration error:", error);
         setApiErrors({ 
            general: "An error occurred during registration. Please try again." 
         });
      }

      setSubmitting(false);
   };

   return (
      <div className="bg-gray-100 min-h-screen">
         <div className="pt-1">
            <Formik
               initialValues={initialValues}
               validationSchema={registerValidationSchema}
               onSubmit={handleSubmit}
            >
               {({ isSubmitting, touched, errors }) => (
                  <Form className="max-w-md mx-auto p-6 pt-1 bg-white rounded shadow-md mt-10">
                     <h1 className="text-center text-2xl my-4 font-bold">
                        SignUp
                     </h1>
                     <hr />

                     {/* Display API/General Errors */}
                     {apiErrors.general && (
                        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
                           {apiErrors.general}
                        </div>
                     )}

                     <div className="flex space-x-4 mt-2">
                        <div className="w-1/2">
                           <InputField
                              name="first_name"
                              label="First Name"
                              touched={touched}
                              errors={{...errors, ...apiErrors}}
                           />
                        </div>
                        <div className="w-1/2">
                           <InputField
                              name="last_name"
                              label="Last Name"
                              touched={touched}
                              errors={{...errors, ...apiErrors}}
                           />
                        </div>
                     </div>
                     <InputField
                        name="username"
                        label="Username"
                        touched={touched}
                        errors={{...errors, ...apiErrors}}
                     />
                     <InputField
                        name="email"
                        label="Email"
                        type="email"
                        touched={touched}
                        errors={{...errors, ...apiErrors}}
                     />

                     <div className="mb-4">
                        <label
                           htmlFor="role"
                           className="block text-gray-700 font-bold mb-2"
                        >
                           Role
                        </label>
                        <Field
                           as="select"
                           name="role"
                           id="role"
                           className={`block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 ${
                              touched.role && errors.role
                                 ? "border-red-500"
                                 : touched.role
                                 ? "border-green-500"
                                 : "border-gray-300"
                           }`}
                        >
                           <option value="job_seeker">Job Seeker</option>
                           <option value="company">Company</option>
                        </Field>
                        <ErrorMessage
                           name="role"
                           component="div"
                           className="text-red-500 text-sm mt-1"
                        />
                     </div>
                     <div className="w-full">
                        <InputField
                           name="password"
                           label="Password"
                           type="password"
                           touched={touched}
                           errors={{...errors, ...apiErrors}}
                        />
                        {apiErrors.password && (
                           <div className="text-red-500 text-sm mt-1">
                              {apiErrors.password}
                           </div>
                        )}
                     </div>

                     {/* Password Requirements */}
                     <div className="text-sm text-gray-600 mt-2 mb-4">
                        <p>Password must:</p>
                        <ul className="list-disc list-inside">
                           <li>Be at least 8 characters long</li>
                           <li>Contain at least one uppercase letter</li>
                           <li>Contain at least one lowercase letter</li>
                           <li>Contain at least one number</li>
                        </ul>
                     </div>

                     <div className="flex flex-col items-center justify-center">
                        <SubmitButton
                           isSubmitting={isSubmitting}
                           text="Signup"
                        />
                        <span className="mt-2">
                           Already have an account?&nbsp;&nbsp;
                           <Link
                              to={"/login"}
                              className="text-blue-600 border-b-2 border-blue-400 hover:text-blue-800"
                           >
                              Login
                           </Link>
                        </span>
                     </div>
                  </Form>
               )}
            </Formik>
         </div>
      </div>
   );
};

export default Register;
