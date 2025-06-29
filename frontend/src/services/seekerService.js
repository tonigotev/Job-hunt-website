import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { axiosInstance } from "./_axiosInstance";

// --------------------
// API Functions
// --------------------

const fetchJobs = async () => {
   const response = await axiosInstance.get("jobs/postings/");
   return response.data;
};

const fetchProfile = async () => {
   const response = await axiosInstance.get("seekers/profiles/my-profile/");
   return response.data;
};

const updateProfile = async (data) => {
   const response = await axiosInstance.patch(
      "seekers/profiles/my-profile/",
      data,
      {
         headers: {
            "Content-Type": "multipart/form-data",
         },
      }
   );
   return response.data;
};

const fetchResumes = async () => {
   const response = await axiosInstance.get("seekers/resumes/");
   return response.data;
};

const createResume = async (data) => {
   const response = await axiosInstance.post("seekers/resumes/", data, {
      headers: {
         "Content-Type": "multipart/form-data",
      },
   });
   return response.data;
};

const deleteResume = async (id) => {
   const response = await axiosInstance.delete(`seekers/resumes/${id}/`);
   return response.data;
};

const fetchExperiences = async () => {
   const response = await axiosInstance.get("seekers/experiences/");
   return response.data;
};

const createExperience = async (data) => {
   const response = await axiosInstance.post("seekers/experiences/", data);
   return response.data;
};

const deleteExperience = async (id) => {
   const response = await axiosInstance.delete(`seekers/experiences/${id}/`);
   return response.data;
};

const updateExperience = async (data) => {
   const response = await axiosInstance.patch(
      `seekers/experiences/${data.id}/`,
      data
   );
   return response.data;
};

const fetchApplications = async () => {
   const response = await axiosInstance.get("jobs/applications/");
   return response.data;
};

const applyJob = async (data) => {
   const response = await axiosInstance.post(`jobs/applications/`, data);
   return response.data;
};

const fetchFilteredJobs = async (params) => {
   console.log("requesting...");
   const response = await axiosInstance.get("jobs/postings/", {
      params: { ...params },
   });
   return response.data;
};

// --------------------
// Custom Hooks
// --------------------

const useFetchJobsQuery = () => {
   return useQuery({
      queryKey: ["allJobs"],
      queryFn: fetchJobs,
      staleTime: 5 * 60 * 1000,
   });
};

const useFetchProfileQuery = () => {
   return useQuery({
      queryKey: ["profile"],
      queryFn: fetchProfile,
      staleTime: 5 * 60 * 1000,
   });
};

const useUpdateProfileMutation = () => {
   const queryClient = useQueryClient();

   return useMutation({
      mutationFn: updateProfile,
      onSuccess: () => {
         queryClient.invalidateQueries("profile");
      },
      onError: (error) => {
         console.error("Error creating profile:", error);
      },
   });
};

const useFetchResumesQuery = () => {
   return useQuery({
      queryKey: ["resumes"],
      queryFn: fetchResumes,
      staleTime: 5 * 60 * 1000,
   });
};

const useCreateResumeMutation = () => {
   const queryClient = useQueryClient();

   return useMutation({
      mutationFn: createResume,
      onMutate: async (newResume) => {
         // optimistic updates
         await queryClient.cancelQueries({ queryKey: ["resumes"] }); // cancels any ongoing refetches
         const previousResumes = queryClient.getQueryData(["resumes"]);
         queryClient.setQueryData(["resumes"], (old) => [...old, newResume]);
         return { previousResumes };
         // If we use only invalidateQueries, there is a delay for server response
      },
      onError: (err, newResume, context) => {
         console.log(err);
         queryClient.setQueryData(["resumes"], context.previousResumes);
      },
      onSettled: () => {
         queryClient.invalidateQueries({ queryKey: ["resumes"] });
      },
   });
};

const useDeleteResumeMutation = () => {
   const queryClient = useQueryClient();

   return useMutation({
      mutationFn: deleteResume,
      onMutate: async (resumeId) => {
         // Optimistically update cache before mutation
         await queryClient.cancelQueries({ queryKey: ["resumes"] });
         const previousResumes = queryClient.getQueryData(["resumes"]);
         queryClient.setQueryData(["resumes"], (oldResumes) =>
            oldResumes.filter((resume) => resume.id !== resumeId)
         );

         return { previousResumes };
      },
      onError: (err, resumeId, context) => {
         queryClient.setQueryData(["resumes"], context.previousResumes);
      },
      onSettled: () => {
         queryClient.invalidateQueries({ queryKey: ["resumes"] });
      },
   });
};

const useFetchExperiencesQuery = () => {
   return useQuery({
      queryKey: ["experiences"],
      queryFn: fetchExperiences,
      staleTime: 5 * 60 * 1000,
   });
};

const useCreateExperienceMutation = () => {
   const queryClient = useQueryClient();

   return useMutation({
      mutationFn: createExperience,
      onMutate: async (newExp) => {
         await queryClient.cancelQueries({ queryKey: ["experiences"] });
         const previousExperiences = queryClient.getQueryData(["experiences"]);
         queryClient.setQueryData(["experiences"], (old) => [...old, newExp]);
         return { previousExperiences };
      },
      onError: (err, newExp, context) => {
         console.log(err);
         queryClient.setQueryData(["experiences"], context.previousExperiences);
      },
      onSettled: () => {
         queryClient.invalidateQueries({ queryKey: ["experiences"] });
      },
   });
};

const useDeleteExperienceMutation = () => {
   const queryClient = useQueryClient();

   return useMutation({
      mutationFn: deleteExperience,
      onMutate: async (expId) => {
         await queryClient.cancelQueries({ queryKey: ["experiences"] });
         const previousExps = queryClient.getQueryData(["experiences"]);
         queryClient.setQueryData(["experiences"], (oldExps) =>
            oldExps.filter((exp) => exp.id !== expId)
         );

         return { previousExps };
      },
      onError: (err, expId, context) => {
         queryClient.setQueryData(["experiences"], context.previousExps);
      },
      onSettled: () => {
         queryClient.invalidateQueries({ queryKey: ["experiences"] });
      },
   });
};

const useUpdateExperienceMutation = () => {
   const queryClient = useQueryClient();

   return useMutation({
      mutationFn: updateExperience,
      onMutate: async (updatedExp) => {
         console.log("values from service:", updatedExp);
         await queryClient.cancelQueries({ queryKey: ["experiences"] });
         const previousExps = queryClient.getQueryData(["experiences"]);

         queryClient.setQueryData(["experiences"], (oldExps) =>
            oldExps.map((exp) =>
               exp.id === updatedExp.id ? { ...exp, ...updatedExp } : exp
            )
         );

         return { previousExps };
      },
      onError: (err, updatedExp, context) => {
         console.log(err);
         queryClient.setQueryData(["experiences"], context.previousExps);
      },
      onSettled: () => {
         queryClient.invalidateQueries({ queryKey: ["experiences"] });
      },
   });
};

const useFetchApplicationsQuery = () => {
   return useQuery({
      queryKey: ["applications"],
      queryFn: fetchApplications,
      staleTime: 5 * 60 * 1000,
   });
};

const useCreateApplicationMutation = () => {
   const queryClient = useQueryClient();

   return useMutation({
      mutationFn: applyJob,
      onSuccess: () => {
         queryClient.invalidateQueries(["applications"]);
      },
      onError: (err) => {
         console.log(err);
      },
   });
};

const useFetchFilteredJobsQuery = (params) => {
   return useQuery({
      queryKey: ["filteredJobs", { ...params }],
      queryFn: () => fetchFilteredJobs(params),
      staleTime: 5 * 60 * 1000,
      keepPreviousData: true,
   });
};

export {
   useFetchJobsQuery,
   useFetchProfileQuery,
   useUpdateProfileMutation,
   useFetchResumesQuery,
   useCreateResumeMutation,
   useDeleteResumeMutation,
   useFetchExperiencesQuery,
   useCreateExperienceMutation,
   useDeleteExperienceMutation,
   useUpdateExperienceMutation,
   useFetchApplicationsQuery,
   useCreateApplicationMutation,
   useFetchFilteredJobsQuery,
};
