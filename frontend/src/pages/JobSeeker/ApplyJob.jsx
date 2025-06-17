import React, { useState } from "react";
import { useCreateApplicationMutation, useFetchResumesQuery } from "../../services/seekerService";
import { IoMdCloseCircleOutline } from "react-icons/io";
import { Formik, Field, Form, ErrorMessage } from "formik";
import { useNavigate } from "react-router-dom";

const ApplyJob = ({ setIsApplying, jobId }) => {
   const { mutate } = useCreateApplicationMutation();
   const { data: resumes = [] } = useFetchResumesQuery();
   const navigate = useNavigate();
   const [errorMessage, setErrorMessage] = useState("");

   const handleSubmit = (values, { setSubmitting }) => {
      const payload = {
         job: jobId,
         cover_letter: values.cover_letter,
         resume_id: values.resume_id,
      };

      mutate(payload, {
         onSuccess: () => {
            setIsApplying(false);
            navigate("/");
            setSubmitting(false);
            setErrorMessage("");
         },
         onError: (error) => {
            if (error.response?.data?.non_field_errors) {
               setErrorMessage(error.response.data.non_field_errors[0]);
            } else if (typeof error.response?.data === "string") {
               setErrorMessage(error.response.data);
            } else {
               setErrorMessage("Unable to apply for job.");
            }
            setSubmitting(false);
         },
      });
   };

   return (
      <Formik
         initialValues={{
            resume_id: "",
            cover_letter: "",
         }}
         onSubmit={handleSubmit}
      >
         {({ isSubmitting }) => (
            <Form className="lg:w-3/5 xl:w-2/5 mx-auto bg-white rounded-lg shadow-lg p-6 relative">
               {errorMessage && (
                  <p className="text-center mx-auto w-3/5 p-2 border border-red-300 mb-4 text-red-500 text-sm">
                     {errorMessage}
                  </p>
               )}

               <div className="grid grid-cols-1 md:grid-cols-2 gap-x-6 items-start">
                  <div>
                     <div className="border rounded-md border-blue-200 px-3">
                        <p className="text-center font-bold text-gray-600 p-3">
                           Select Resume
                        </p>
                        <hr />
                        <Field
                           as="select"
                           name="resume_id"
                           className="w-full my-2 text-sm p-2.5 text-gray-800 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
                        >
                           <option value="">-- Choose resume --</option>
                           {resumes.map((res) => (
                              <option key={res.id} value={res.id}>
                                 {res.resume_title}
                              </option>
                           ))}
                        </Field>
                        <ErrorMessage
                           name="resume_id"
                           component="div"
                           className="text-red-500 text-sm mt-1"
                        />
                     </div>
                  </div>

                  {/* Cover Letter */}
                  <div className="border rounded-md border-blue-200 px-3">
                     <p className="text-center font-bold text-gray-600 p-3">
                        Cover Letter
                     </p>
                     <hr />
                     <Field
                        as="textarea"
                        name="cover_letter"
                        cols="33"
                        rows="5"
                        placeholder="Write your cover letter here..."
                        className="w-full my-2 text-sm p-2.5 text-gray-800 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
                     />
                     <ErrorMessage
                        name="cover_letter"
                        component="div"
                        className="text-red-500 text-sm mt-1"
                     />
                  </div>
               </div>

               {/* Submit Button */}
               <div className="flex justify-center md:justify-end md:mr-32">
                  <button
                     type="submit"
                     className="bg-indigo-500 text-white px-4 py-2 rounded-md text-xs hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 mt-4 md:mt-1"
                     disabled={isSubmitting}
                  >
                     {isSubmitting ? "loading" : "Apply"}
                  </button>
               </div>

               {/* Close Button */}
               <IoMdCloseCircleOutline
                  onClick={() => setIsApplying(false)}
                  className="text-red-600 cursor-pointer absolute right-1 top-1"
                  size={21}
               />
            </Form>
         )}
      </Formik>
   );
};

export default ApplyJob;
