import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { axiosInstance } from "./_axiosInstance";

// --------------------
// API Functions
// --------------------

const createJob = async (jobData) => {
   const response = await axiosInstance.post("jobs/postings/", jobData);
   return response.data;
};

const fetchJobsByCompany = async () => {
   const response = await axiosInstance.get("jobs/postings/my-jobs/");
   return response.data;
};

const fetchJob = async (jobId) => {
   const response = await axiosInstance.get(`jobs/postings/${jobId}/`);
   return response.data;
};

const updateJob = async ({ jobId, jobData }) => {
   const response = await axiosInstance.patch(
      `jobs/postings/${jobId}/`,
      jobData
   );
   return response.data;
};

const fetchFilteredApplications = async ({jobId, status}) => {
   const params = { job: jobId };
   if (status && status !== 'all') {
      params.status = status;
   }
   const response = await axiosInstance.get(
      `jobs/applications/`,
      { params }
   );
   return response.data;
};

const updateApplication = async ({ applicationId, data }) => {
   const response = await axiosInstance.patch(
      `jobs/applications/${applicationId}/update-status/`,
      data
   );
   return response.data;
};


// --------------------
// Custom Hooks
// --------------------

const useCreateJobMutation = () => {
   const queryClient = useQueryClient();

   return useMutation({
      mutationFn: createJob,
      onSuccess: (data) => {
         queryClient.invalidateQueries({ queryKey: ["company-jobs"] });
         console.log("Job created successfully:", data);
      },
      onError: (error) => {
         console.error("Error creating job:", error);
      },
   });
};

const useFetchJobsByCompanyQuery = () => {
    return useQuery({
       queryKey: ["company-jobs"],
       queryFn: fetchJobsByCompany,
       staleTime: 5 * 60 * 1000,
    });
 };

const useFetchJobQuery = (jobId) => {
   return useQuery({
      queryKey: ["job", jobId],
      queryFn: () => fetchJob(jobId),
      staleTime: 5 * 60 * 1000,
      enabled: !!jobId,
   });
};

const useUpdateJobMutation = () => {
   const queryClient = useQueryClient();

   return useMutation({
      mutationFn: updateJob,
      onSuccess: (data, variables) => {
         queryClient.invalidateQueries({ queryKey: ["job", variables.jobId] });
         queryClient.invalidateQueries({ queryKey: ["company-jobs"] });
      },
      onError: (error) => {
         console.error("Error updating job:", error);
      },
   });
};

const useFilteredApplicationsQuery = (jobId, status) => {
   return useQuery({
      queryKey: ["applications", jobId, status],
      queryFn: () => fetchFilteredApplications({jobId, status}),
      enabled: !!jobId,
      staleTime: 5 * 60 * 1000,
   });
};

const useUpdateApplicationMutation = (jobId, status) => {
   const queryClient = useQueryClient();

   return useMutation({
      mutationFn: updateApplication,
      onSuccess: () => {
         queryClient.invalidateQueries({ queryKey: ["applications", jobId] });
      },
      onError: (err) => {
         console.error("Error:", err);
      },
   });
};


export {
   useCreateJobMutation,
   useFetchJobsByCompanyQuery,
   useFetchJobQuery,
   useUpdateJobMutation,
   useFilteredApplicationsQuery,
   useUpdateApplicationMutation,
}; 