@share_bp.route('/consent/<int:id>', methods=['POST'])
def give_consent(id):
    response = SurveyResponse.query.get(id)
    if response.user_id == current_user.id:
        response.shared = True
        db.session.commit()
        flash('Your result is now public.', 'success')
