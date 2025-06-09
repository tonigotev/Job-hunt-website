import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { useFetchJobQuery } from "../services/companyService";
import { useGetUserQuery } from "../services/authService";
import UpdateJob from "../components/UpdateJob";
import ApplyJob from "./JobSeeker/ApplyJob";

const JobDetails = () => {
   const { jobId } = useParams();
   const [userRole, setUserRole] = useState("");
   const [showUpdation, setShowUpdation] = useState(false);
   const [isApplying, setIsApplying] = useState(false);

   const { data: user, isLoading: isLoadingUser } = useGetUserQuery();
   const { data, isLoading, isError, error } = useFetchJobQuery(jobId);

   useEffect(() => {
      if (user && data) {
         if (user.role === "job_seeker") {
            setUserRole("seeker");
         } else if (user.role === "admin") {
            setUserRole("admin");
         } else if (user.role === "company") {
            if (user.id === data.company.user.id) {
               setUserRole("owner");
            }
         }
      }
   }, [user, data]);

   if (isLoading || isLoadingUser) {
      return <div>Loading job details...</div>;
   }

   if (isError) {
      return <div>Error: {error.message}</div>;
   }

   return (
      <>
         {!showUpdation ? (
            <div className="flex justify-center">
               <div className="w-full lg:w-2/6 bg-white shadow-md rounded-lg p-6 my-4">
                  <div className="flex justify-between">
                     <h2 className="text-2xl font-semibold text-gray-800 mb-4">
                        {data.title}
                     </h2>
                     <p className="text-lg text-gray-600 mb-2">
                        {data.company.title}
                     </p>
                  </div>
                  <div className="mx-20">
                     <p className="text-md text-gray-600 mb-2">
                        <strong className="mr-2">Date Posted:</strong>
                        {new Date(data.date_posted).toLocaleDateString()}
                     </p>
                     <p className="text-md text-gray-600 mb-2">
                        <strong className="mr-2">Last Date to Apply:</strong>
                        {new Date(data.last_date_to_apply).toLocaleDateString()}
                     </p>
                     <p className="text-md text-gray-600 mb-2">
                        <strong className="mr-2">Employment Type:</strong>
                        {data.employment_type}
                     </p>
                     <p className="text-md text-gray-600 mb-2">
                        <strong className="mr-2">Salary:</strong> {data.salary}
                     </p>
                     <p className="text-md text-gray-600 mb-2">
                        <strong className="mr-2">Vacancy:</strong>{" "}
                        {data.vacancy}
                     </p>
                     <p className="text-md text-gray-600 mb-2">
                        <strong className="mr-2">Description:</strong>
                        {data.description}
                     </p>
                  </div>

                  {userRole === "seeker" && !isApplying && (
                     <div className="flex justify-center">
                        <button
                           onClick={() => setIsApplying(true)}
                           className="text-sm sm:text-base bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition-colors duration-300"
                        >
                           Apply Job
                        </button>
                     </div>
                  )}

                  {userRole === "admin" ||
                     (userRole === "owner" && (
                        <div className="flex justify-center">
                           <button
                              onClick={() => setShowUpdation(true)}
                              className="text-sm sm:text-base bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition-colors duration-300"
                           >
                              Update Job
                           </button>
                        </div>
                     ))}
               </div>
            </div>
         ) : (
            <UpdateJob jobDetails={data} toggle={setShowUpdation} />
         )}

         {isApplying && (
            <ApplyJob setIsApplying={setIsApplying} jobId={jobId} />
         )}
      </>
   );
};

export default JobDetails;
