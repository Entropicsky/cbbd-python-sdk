                            else:
                                st.warning("No valid height and weight data found after filtering.")
                        else:
                            st.warning("Height and weight data not available for this team.")
                    
                    with roster_viz_tab3:
                        st.subheader("Position Breakdown")
                        
                        if has_position_data:
                            # Position distribution
                            pos_counts = roster_df["Position"].value_counts().reset_index()
                            pos_counts.columns = ["Position", "Count"]
                            
                            if len(pos_counts) > 1:  # Only create chart if we have multiple positions
                                # Pie chart for positions
                                position_fig, ax = plt.subplots(figsize=(8, 8))
                                ax.pie(pos_counts["Count"], labels=pos_counts["Position"], autopct='%1.1f%%', 
                                      startangle=90, shadow=False)
                                ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
                                plt.title(f"Position Breakdown for {team} ({season})")
                                st.pyplot(position_fig)
                            
                            # Table of players by position
                            st.subheader("Players by Position")
                            for position in pos_counts["Position"]:
                                position_players = roster_df[roster_df["Position"] == position]
                                st.markdown(f"**{position}** ({len(position_players)}): " + 
                                            ", ".join(position_players["Name"].tolist()))

                            # Position breakdown
                            for position in sorted(roster_df["Position"].unique()):
                                position_players = roster_df[roster_df["Position"] == position].sort_values("Jersey")
                                st.markdown(f"**{position}** ({len(position_players)}): " + 
                                        ", ".join(position_players["Name"].tolist()))
                            
                            # Position experience breakdown - only if we have experience data
                            if "Experience" in roster_df.columns and not roster_df["Experience"].isna().all():
                                exp_by_pos = roster_df.groupby("Position")["Experience"].mean().reset_index()
                                exp_by_pos.columns = ["Position", "Avg Experience"]
                                
                                if len(exp_by_pos) > 1:  # Only create chart if we have multiple positions
                                    exp_chart = alt.Chart(exp_by_pos).mark_bar().encode(
                                        x=alt.X("Position:N"),
                                        y=alt.Y("Avg Experience:Q"),
                                        color=alt.Color("Position:N", scale=alt.Scale(scheme="category10")),
                                        tooltip=["Position", "Avg Experience"]
                                    ).properties(
                                        title="Average Experience by Position (Years)",
                                        width=600,
                                        height=300
                                    )
                                    
                                    st.altair_chart(exp_chart, use_container_width=True)
                            else:
                                st.warning("Position data not available or uniform for this team.")
                 else:
                     st.warning(f"No roster data found for {team} in {season}.")
         except Exception as e:
             st.error(f"Error loading roster data: {e}")
             import traceback
             st.text(traceback.format_exc())
