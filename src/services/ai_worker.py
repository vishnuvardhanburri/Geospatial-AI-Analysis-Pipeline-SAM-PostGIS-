@celery.task(bind=True, max_retries=3)
def segment_map_task(self, image_bytes):
    # Confidence-gated execution to ensure measurement integrity
    masks = sam_model.predict(image_bytes)
    validated_features = [m for m in masks if m.score > 0.85] 
    
    if not validated_features:
        # Senior move: Trigger Human-in-the-loop instead of guessing
        return trigger_manual_review(image_bytes)
    
    return process_geospatial_results(validated_features)
