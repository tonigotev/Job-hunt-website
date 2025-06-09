import React, { useState } from "react";
import JobCard from "../../components/JobCard";
import { useFetchMyCompanyQuery } from "../../services/companyService";
import { useFetchJobsByCompanyQuery } from "../../services/jobService";
import CompanyForm from "../../components/company/CompanyForm";
import JobForm from "../../components/company/JobForm";
import { useGetUserQuery } from "../../services/authService";
import ProfileCard from "../../components/company/ProfileCard";
import UserCard from "../../components/UserCard";
import UpdateUserForm from "../../components/company/UpdateUserForm";

const CompanyProfile = () => {
   const [activeSection, setActiveSection] = useState("jobs");
   const [isCompanyModalOpen, setCompanyModalOpen] = useState(false);
   const { data: user } = useGetUserQuery();

   const {
      data: companyData,
      isLoading: companyLoading,
      error: companyError,
   } = useFetchMyCompanyQuery();

   const {
      data: jobsData,
      isLoading: jobsLoading,
      error: jobsError,
   } = useFetchJobsByCompanyQuery();

   const companyDetails = {
      title: companyData?.title || "",
      location: companyData?.location || "",
      website: companyData?.website || "",
      established_date: companyData?.established_date || "",
      description: companyData?.description || "",
   };

   const handleSectionChange = (section) => {
      setActiveSection(section);
   };

   if (companyLoading || jobsLoading) return <div>Loading...</div>;
   if (companyError) return <div>Error: {companyError.message}</div>;
   if (jobsError) return <div>Error: {jobsError.message}</div>;

   return (
      <>
         <div className="lg:flex justify-evenly">
            <ProfileCard
               initialValues={companyDetails}
               onEdit={() => handleSectionChange("updateCompany")}
               onAddJob={() => handleSectionChange("addJob")}
            />
            <UserCard
               user={user}
               onEdit={() => handleSectionChange("updateUser")}
            />
         </div>
         {activeSection === "jobs" && (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-x-4 gap-y-6 md:gap-y-20 p-6 mt-4 mx-0 lg:mx-20">
               {jobsData?.map((job) => (
                  <JobCard key={job.id} btn_text={"Open"} job={job} />
               ))}
            </div>
         )}
         {activeSection === "updateCompany" && (
            <CompanyForm
               initialValues={companyDetails}
               onClick={() => handleSectionChange("jobs")}
            />
         )}
         {activeSection === "updateUser" && (
            <UpdateUserForm
               user={user}
               onClick={() => handleSectionChange("jobs")}
            />
         )}
         {activeSection === "addJob" && (
            <JobForm onClick={() => handleSectionChange("jobs")} />
         )}
      </>
   );
};

export default CompanyProfile;
