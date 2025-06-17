import React from "react";
import { useLocation } from "react-router-dom";

const SeekerProfile = () => {
   const location = useLocation();
   const { seeker } = location.state || {};

   if (!seeker) {
      return (
         <div className="flex flex-col items-center mt-10">
            <p className="text-gray-600">No seeker data provided.</p>
            <p className="text-gray-500 text-sm mt-2">
               Try navigating from the Job-Seekers list.
            </p>
         </div>
      );
   }

   return (
      <div className="lg:w-3/5 xl:w-2/5 mx-auto bg-white rounded-lg shadow-lg p-6 mt-4">
         <h2 className="text-3xl font-bold text-slate-700 mb-4">
            {seeker.get_full_name}
         </h2>
         <div className="space-y-2 text-gray-700">
            <p>
               <span className="font-semibold">Username:</span> {seeker.username}
            </p>
            <p>
               <span className="font-semibold">Email:</span> {seeker.email}
            </p>
         </div>
      </div>
   );
};

export default SeekerProfile; 