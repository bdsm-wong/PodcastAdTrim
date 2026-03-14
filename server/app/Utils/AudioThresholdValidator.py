class AudioThresholdValidator:
    @staticmethod
    def sound_threshold_limit(matrix_audio, min=0, max=1):
        total_threshold = 0.0
        
        for sample in matrix_audio:
            total_threshold += abs(sample)
        average = total_threshold / len(matrix_audio) if total_threshold > 0 else 0.0

        limit = average > float(min) and average < float(max)

        if limit: return {"error": False, 
                          "message": average
                        }
        else: return {
                "error": True, 
                "message": f"The audio is not at the appropriate volume. Average normalized amplitude: {average}",
            }
        