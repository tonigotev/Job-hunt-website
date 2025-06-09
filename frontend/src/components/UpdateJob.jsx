import { ErrorMessage, Field, Form, Formik } from "formik";
import InputField from "./InputField";
import SubmitButton from "./SubmitButton";
import { JobFormValidationSchema } from "../utils/validationSchemas";
import { IoCloseSharp } from "react-icons/io5";
import { useUpdateJobMutation } from "../services/companyService";

const UpdateJob = ({ jobDetails, toggle }) => {
   const updateJobMutation = useUpdateJobMutation();

   const initialValues = {
      title: jobDetails.title,
      salary: jobDetails.salary,
      vacancy: jobDetails.vacancy,
      description: jobDetails.description,
      employment_type: jobDetails.employment_type,
      last_date_to_apply: jobDetails.last_date_to_apply,
   };

   const handleSubmit = (values, { setSubmitting, setFieldError }) => {
      const filteredValues = Object.fromEntries(
         Object.entries(values).map(([key, value]) => [
            key,
            value === "" ? null : value,
         ])
      );

      updateJobMutation.mutate(
         {
            jobId: jobDetails.id,
            jobData: filteredValues,
         },
         {
            onSuccess: () => {
               toggle(false);
            },
            onError: (error) => {
               if (error.response && error.response.data) {
                  const errors = error.response.data;
                  Object.keys(errors).forEach((field) => {
                     setFieldError(field, errors[field][0]);
                  });
               }
            },
         }
      );
      setSubmitting(false);
   };

   return (
      <Formik
         initialValues={initialValues}
         validationSchema={JobFormValidationSchema}
         onSubmit={handleSubmit}
      >
         {({ isSubmitting, touched, errors }) => (
            <Form className="max-w-lg mx-auto p-6 pt-1 bg-white rounded shadow-md mt-6 relative">
               <h1 className="text-center text-2xl my-4 font-bold">
                  Update Job
               </h1>
               <hr />
               <div className="flex space-x-11 mt-2">
                  <InputField
                     name="title"
                     label="Job Title"
                     touched={touched}
                     errors={errors}
                  />
                  <InputField
                     name="salary"
                     label="Salary"
                     touched={touched}
                     errors={errors}
                  />
               </div>
               <div className="flex space-x-11 mt-2">
                  <InputField
                     name="vacancy"
                     label="Vacancy"
                     touched={touched}
                     errors={errors}
                  />

                  <div>
                     <label
                        htmlFor="employment_type"
                        className="block text-gray-700 font-bold mb-2"
                     >
                        Role
                     </label>
                     <Field
                        as="select"
                        name="employment_type"
                        id="employment_type"
                        className={`block w-52 px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 ${
                           touched.employment_type && errors.employment_type
                              ? "border-red-500"
                              : touched.employment_type
                              ? "border-green-500"
                              : "border-gray-300"
                        }`}
                     >
                        <option value="Full-time">Full time</option>
                        <option value="Part-time">Part time</option>
                        <option value="Contract">Contract</option>
                        <option value="Freelance">Freelance</option>
                        <option value="Internship">Internship</option>
                     </Field>
                  </div>
               </div>
               <InputField
                  name="last_date_to_apply"
                  label="Last date to apply"
                  touched={touched}
                  errors={errors}
                  type="date"
               />
               <div className="mb-4">
                  <label
                     htmlFor="description"
                     className="block text-gray-700 font-bold mb-2"
                  >
                     Description
                  </label>
                  <Field
                     as="textarea"
                     name="description"
                     id="description"
                     cols="5"
                     rows="3"
                     className={`block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 ${
                        touched.description && errors.description
                           ? "border-red-500"
                           : touched.description
                           ? "border-green-500"
                           : "border-gray-300"
                     }`}
                  />
                  <ErrorMessage
                     name="description"
                     component="div"
                     className="text-red-500 text-sm mt-1"
                  />
               </div>

               <div className="flex items-center justify-between">
                  <SubmitButton isSubmitting={isSubmitting} text="Add Job" />
               </div>

               <button
                  onClick={() => toggle(false)}
                  className="absolute top-2 right-2 rounded-full bg-zinc-100 p-1 text-2xl text-red-400 hover:bg-zinc-200 hover:text-red-600 shadow-xl transition-shadow duration-300"
               >
                  <IoCloseSharp />
               </button>
            </Form>
         )}
      </Formik>
   );
};

export default UpdateJob;
